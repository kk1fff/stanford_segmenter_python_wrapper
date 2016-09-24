import subprocess
import os

class StanfordSegmenter:
    CLASS_NAME = "info.ckwang.util.segmenter_wrapper.App"

    def __init__(self,
                 path_to_wrapper,
                 path_to_jar,
                 path_to_slf4j,
                 path_to_sihan_corpora_dict,
                 path_to_model,
                 path_to_dict):
        self._path_to_jar = path_to_jar
        self._path_to_slf4j = path_to_slf4j
        self._path_to_sihan_corpora_dict = path_to_sihan_corpora_dict
        self._path_to_model = path_to_model
        self._path_to_dict = path_to_dict
        self._path_to_wrapper = path_to_wrapper
        self._proc = None

    def segment(self, text):
        if self._proc == None:
            # start the subprocess
            self._run_proc()

        self._proc.stdin.write(text.strip() + "\n")
        self._proc.stdin.flush()
        # wait for output
        r = self._proc.stdout.readline()
        return r

    def _run_proc(self):
        path_to_wrapper_dir = os.path.dirname(os.path.abspath(self._path_to_wrapper))
        path_to_jar_dir = os.path.dirname(os.path.abspath(self._path_to_jar))
        path_to_slf4j_dir = os.path.dirname(os.path.abspath(self._path_to_slf4j))
        self._proc = subprocess.Popen(
            ['java',
             '-cp',
             ':'.join([ os.path.join(path_to_wrapper_dir, "*"),
                        os.path.join(path_to_jar_dir, "*"),
                        os.path.join(path_to_slf4j_dir, "*") ]),
             StanfordSegmenter.CLASS_NAME,
             self._path_to_sihan_corpora_dict,
             self._path_to_dict,
             self._path_to_model],
            universal_newlines = True,
            env=dict(os.environ, **{
                "CLASSPATH": path_to_jar_dir + ":" + path_to_slf4j_dir + ":" + path_to_wrapper_dir
            }),
            stdout = subprocess.PIPE,
            stdin = subprocess.PIPE,
            stderr = open(os.devnull, 'w'))

    def end(self):
        if self._proc != None:
            self._proc.stdin.close()
            self._proc.wait()
            self._proc = None

    def __del__(self):
        self.end()

