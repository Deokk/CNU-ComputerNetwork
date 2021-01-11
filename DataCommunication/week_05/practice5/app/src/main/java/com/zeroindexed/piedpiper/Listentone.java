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
    int HANDSHAKE_START_HZ = 8192; // 알맞은 값 추가할 것
    int HANDSHAKE_END_HZ = 8192 + 512; // 알맞은 값 추가할 것

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
        int count = 1,result = 0, sub_val = 0;
        while(true) {
            result = (int)Math.pow(2, count);
            sub_val = size - result;
            if(sub_val < 0) {
                break;
            }
            count++;
        }

        return (int)Math.pow(2, count-1);
    }

    public void Listen_main() {
        String StringData = null;
        this.mAudioRecord.startRecording();

        System.out.println("ssss");

        boolean in_packet = false;
        int blockSize = FindPowerSize(Math.round((interval / 2) * mSampleRate));    // 채워넣음
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

            if(in_packet && match(dom, HANDSHAKE_END_HZ)) {
                //
                Log.d("CHECK", "The frequency in the ArrayList.");
                for(int i = 0; i < packet.size(); i++) {
                    /**
                     *  시작 주파수는 출력x
                     *  packet에 들어온 주파수 출력
                     */
                    if (!match(packet.get(i), HANDSHAKE_START_HZ)
                            && !match(packet.get(i), HANDSHAKE_END_HZ))
                        System.out.println(packet.get(i));
                }
                break;
            } else if(in_packet) {
                // packet ArrayList에 주파수 추가
                packet.add(dom);
            } else if(match(dom, HANDSHAKE_START_HZ)) {
                // HANDSHAKE_START_HZ가 들어왔음을 확인 (True)
                in_packet = true;
            }
        }
        this.mAudioRecord.stop();
    }

    private boolean match(double freq1, double freq2) {
        return Math.abs(freq1 - freq2) < 20;
    }

    // https://github.com/numpy/numpy/blob/v1.17.0/numpy/fft/helper.py#L126-L172
    // 반환하는 모양은 아래와 같다. (n == len, d == duration)
    // f = [0, 1, ...,   n/2-1,     -n/2, ..., -1] / (d*n)   if n is even
    // f = [0, 1, ..., (n-1)/2, -(n-1)/2, ..., -1] / (d*n)   if n is odd
    private Double[] fft(int len, int duration) {
        // val과 results는 참고용 (수정해서 구현해도 상관없음)
        Double val = 1.0 / (len * duration);
        Double[] results = new Double[len];
        /****************************************

         ------------INPUT YOUR CODE-------------

         ****************************************/
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

        for(int i = 0; i< complex.length; i++) {
            realNum = complex[i].getReal();
            imgNum = complex[i].getImaginary();
            complex_val[i] = Math.sqrt((realNum * realNum) + (imgNum * imgNum));
        }

        Double max;
        int maxIndex = 0;
        /*************************************

         ---------maxIndex를 찾는 과정--------
         pied_piper의 decode.py 파일의 dominant함수 참고
         -> peak_coeff = np.argmax(np.abs(w))
            peak_freq = freqs[peak_coeff]
            return abs(peak_freq * frame_rate)

         *************************************/

        for (int i = 0; i < complex_val.length; i ++) {
            if (complex_val[maxIndex] < complex_val[i])
                maxIndex = i;
        }
        max = freq[maxIndex];

        return Math.abs(max * mSampleRate);
    }
}
