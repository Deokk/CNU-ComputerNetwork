package com.zeroindexed.piedpiper;

import android.media.AudioFormat;
import android.media.AudioRecord;
import android.media.MediaRecorder;
import android.util.Log;

import org.apache.commons.math3.complex.Complex;
import org.apache.commons.math3.transform.DftNormalization;
import org.apache.commons.math3.transform.FastFourierTransformer;
import org.apache.commons.math3.transform.TransformType;

import java.util.ArrayList;

public class Listentone {
    int HANDSHAKE_START_HZ = 8192;
    int HANDSHAKE_END_HZ = 8192 + 512;

    int START_HZ = 1024;
    int STEP_HZ = 256;
    int BITS = 4;

    private int mAudioSource = MediaRecorder.AudioSource.MIC;
    private int mSampleRate = 44100;
    private int mChannelCount = AudioFormat.CHANNEL_IN_MONO;
    private int mAudioFormat = AudioFormat.ENCODING_PCM_16BIT;
    private float interval = 0.1f;

    private int mBufferSize = AudioRecord.getMinBufferSize(mSampleRate, mChannelCount, mAudioFormat);

    FastFourierTransformer transform;
    public AudioRecord mAudioRecord = null;

    public Listentone() {
        transform = new FastFourierTransformer(DftNormalization.STANDARD);
        mAudioRecord = new AudioRecord(mAudioSource, mSampleRate, mChannelCount, mAudioFormat, mBufferSize);
    }

    private int FindPowerSize(int size) {
        int count = 1, result = 0, sub_val = 0;
        while (true) {
            result = (int) Math.pow(2, count);
            sub_val = size - result;
            if (sub_val < 0) {
                break;
            }
            count++;
        }

        return (int) Math.pow(2, count - 1);
    }

    public void Listen_main() {
        String StringData = null;
        this.mAudioRecord.startRecording();

        boolean in_packet = false;
        int blockSize = FindPowerSize(Math.round((interval / 2) * mSampleRate));
        ArrayList<Double> packet = new ArrayList<>();
        short[] buffer = new short[blockSize];

        double[] toTransform = new double[blockSize];
        while (true) {
            int bufferedReadResult = mAudioRecord.read(buffer, 0, blockSize);
            if (bufferedReadResult < 0) break;

            for (int i = 0; i < blockSize && i < bufferedReadResult; i++) {
                toTransform[i] = (double) buffer[i];
            }

            double dom = dominant(toTransform);

            if (in_packet && match(dom, HANDSHAKE_END_HZ)) {
                Log.d("ListenTone", "end");

                short[] chunk = extract_packet(packet);
                StringData = decodeBitChunk(chunk);
                Log.d("ListenTone Result", StringData);

            } else if (in_packet) {
                packet.add(dom);
            } else if (match(dom, HANDSHAKE_START_HZ)) {
                Log.e("ListenTone - START", "start");
                in_packet = true;
            }
        }
        this.mAudioRecord.stop();
    }

    private String decodeBitChunk(short[] chunk) {
        String allData = "";

        int next_read_chunk = 0;
        int next_read_bit = 0;

        int _byte = 0;
        int bits_left = 8;

        while (next_read_chunk < chunk.length) {

            int can_fill = BITS - next_read_bit;
            int to_fill = Math.min(bits_left, can_fill);
            int offset = BITS - next_read_bit - to_fill;
            _byte <<= to_fill;
            int shifted = chunk[next_read_chunk] & (((1 << to_fill) - 1) << offset);
            _byte |= shifted >> offset;
            bits_left -= to_fill;
            next_read_bit += to_fill;

            if (bits_left <= 0) {
                allData += Character.toString((char)_byte);
                _byte = 0;
                bits_left = 8;
            }

            if (next_read_bit >= BITS) {
                next_read_chunk += 1;
                next_read_bit -= BITS;
            }
        }

        return allData;
    }

    private boolean match(double freq1, double freq2) {
        return Math.abs(freq1 - freq2) < 20;
    }

    private short[] extract_packet(ArrayList<Double> packet) {
        ArrayList<Double> samplingPacket = new ArrayList<>();
        Double[] sampling = new Double[packet.size() / 2 + 1];

        int index_sampling = 0;
        for (int index_packet = 0; index_packet < packet.size(); index_packet++) {
            if (match(packet.get(index_packet), HANDSHAKE_START_HZ)) {
                continue;
            }
            if (index_sampling != 0 && sampling[index_sampling - 1].equals(packet.get(index_packet))) {
                continue;
            }
            else {
                sampling[index_sampling] = packet.get(index_packet);
                samplingPacket.add(packet.get(index_packet));
                index_sampling++;
            }
        }

        for (int i = 0; i < samplingPacket.size(); i++) {
            Log.d("ListenTone relay", Double.toString(samplingPacket.get(i)));
        }

        short[] chunks = new short[samplingPacket.size()];

        for (int i = 0; i < samplingPacket.size(); i++) {
            chunks[i] = (short) Math.round((samplingPacket.get(i) - START_HZ) / STEP_HZ);
        }
        for (int i = 0; i < chunks.length; i++) {
            Log.d("ListenTone chunks", Short.toString(chunks[i]));
        }
        return chunks;
    }

    private Double[] fft(int len, int duration) {
        Double val = 1.0 / (len * duration);
        Double[] results = new Double[len];
        for (int i = 0; i < len / 2; i++)
            results[i] = i * val;
        for (int i = len / 2; i < len; i++)
            results[i] = (i - len) * val;
        return results;
    }

    private double dominant(double[] transform_chunk) {
        int len = transform_chunk.length;
        double realNum;
        double imgNum;
        double[] complex_val = new double[len];

        Complex[] complex = transform.transform(transform_chunk, TransformType.FORWARD);
        Double[] freq = this.fft(complex.length, 1);

        for (int i = 0; i < complex.length; i++) {
            realNum = complex[i].getReal();
            imgNum = complex[i].getImaginary();
            complex_val[i] = Math.sqrt((realNum * realNum) + (imgNum * imgNum));
        }

        Double max = 0D;
        int maxIndex = 0;

        for (int i = 1; i < complex_val.length; i++) {
            if (complex_val[maxIndex] < complex_val[i]) {
                maxIndex = i;
            }
        }

        max = freq[maxIndex];
        return Math.abs(max * mSampleRate);
    }
}