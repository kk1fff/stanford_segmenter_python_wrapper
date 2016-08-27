from segmenter import StanfordSegmenter

if __name__ == "__main__":
    s = StanfordSegmenter(path_to_wrapper = "../stanford-segmenter/wrapper.jar",
                          path_to_jar = "../stanford-segmenter/stanford-segmenter-3.6.0.jar",
                          path_to_slf4j = "../stanford-segmenter/slf4j-api.jar",
                          path_to_sihan_corpora_dict = "../stanford-segmenter/data",
                          path_to_model = "../stanford-segmenter/data/ctb.gz",
                          path_to_dict = "../stanford-segmenter/data/dict-chris6.ser.gz")
    print(s.segment("這是一個實驗"))
    print(s.segment("看看速度如何"))
