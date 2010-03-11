clean = lambda string : string.lower().strip()
has_word = lambda (sentence, word) : clean(word) in clean(sentence).split()
        
    
    
