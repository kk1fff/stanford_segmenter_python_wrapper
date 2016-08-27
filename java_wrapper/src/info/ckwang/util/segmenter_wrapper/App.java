package info.ckwang.util.segmenter_wrapper;

import java.io.*;
import java.util.*;

import edu.stanford.nlp.ie.crf.CRFClassifier;
import edu.stanford.nlp.io.IOUtils;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.objectbank.ObjectBank;
import edu.stanford.nlp.sequences.SeqClassifierFlags;

public class App {

	// arg: <sighanCorporaDict> <serDictionary> <loadClassifier>
	public static void main(String[] args) {
	    Properties props = new Properties();

	    if (args.length != 3) {
	    	System.err.println(String.format("app <sighanCorporaDict> <serDictionary> <loadClassifier>"));
	    	System.exit(1);
	    }
	    
	    // Dictionary path.
	    props.setProperty("sighanCorporaDict", args[0]);
	    props.setProperty("serDictionary", args[1]);
	    props.setProperty("loadClassifier", args[2]);
	    props.setProperty("sighanPostProcessing", "true");

	    SeqClassifierFlags flags = new SeqClassifierFlags(props);
	    CRFClassifier<CoreLabel> crf = new CRFClassifier<>(flags);

	    String loadPath = flags.loadClassifier;
	    
	    crf.loadClassifierNoExceptions(loadPath, props);
	    crf.loadTagIndex();
	    
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
	    try {
	    	while (true) {
	    		String line = br.readLine();
	    		if (line == null || line.isEmpty()) {
	    			break;
	    		}
	    		
	    		ObjectBank<List<CoreLabel>> docs = crf.makeObjectBankFromString(line, crf.defaultReaderAndWriter());
	    		crf.classifyAndWriteAnswers(docs, IOUtils.encodedOutputStreamPrintWriter(System.out, flags.outputEncoding, true), crf.plainTextReaderAndWriter(), false);
	    	}
	    } catch (Exception e) {
	    	System.err.println(e.getMessage());
	    }
	}

}
