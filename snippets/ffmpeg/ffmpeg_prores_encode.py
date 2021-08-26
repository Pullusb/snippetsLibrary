## prores encoding

# using pix format
ffmpeg -i test.mov -c:v prores_ks -pix_fmt yuv422p10 test_422.mov

# using profile
ffmpeg -i input.avi -c:v prores_ks -profile:v 3 -c:a pcm_s16le output.mov

# The -profile switch takes an integer from -1 to 5 to match the ProRes profiles:
#    -1: auto (default)
#    0: proxy ≈ 45Mbps YUV 4:2:2
#    1: lt ≈ 102Mbps YUV 4:2:2
#    2: standard ≈ 147Mbps YUV 4:2:2
#    3: hq ≈ 220Mbps YUV 4:2:2
#    4: 4444≈ 330Mbps YUVA 4:4:4:4
#    5: 4444xq ≈ 500Mbps YUVA 4:4:4:4


# prores with alpha from image sequence:
ffmpeg -f image2 -start_number 1 -i img_%04d.png -r 24 -c:v prores_ks -pix_fmt yuva444p10le -alpha_bits 16 -profile:v 4444 seq_prores_a.mov