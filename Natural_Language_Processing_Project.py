import math

def norm(vec):
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    common_keys=set(vec1.keys()) & set(vec2.keys())
    list_of_common_keys=list(common_keys)
    list_of_keys_in_vec1=list(vec1.keys())
    list_of_keys_in_vec2=list(vec2.keys())
    sum_of_common=0
    sum_of_vec1=0
    sum_of_vec2=0
    for i in range(len(list_of_common_keys)):
        sum_of_common+=vec1.get(list_of_common_keys[i])*vec2.get(list_of_common_keys[i])
    for i in range(len(list_of_keys_in_vec1)):
        sum_of_vec1+=(vec1.get(list_of_keys_in_vec1[i]))**2
    for i in range(len(list_of_keys_in_vec2)):
        sum_of_vec2+=(vec2.get(list_of_keys_in_vec2[i]))**2
    bottom=(sum_of_vec1*sum_of_vec2)**(1/2)

    return sum_of_common/bottom
        
def build_semantic_descriptors(sentences):
    for i in range(len(sentences)):
        for j in range(len(sentences[i])):
            sentences[i][j] = sentences[i][j].lower()
    main_dict={}
    for i in range(len(sentences)):
        for k in range(0,len(sentences[i])):
            new_list=sentences[i].copy()
            new_list.remove(sentences[i][k])
            if sentences[i][k] in main_dict:
                for j in range(len(new_list)):
                    if new_list[j] in main_dict[sentences[i][k]]:
                        main_dict[sentences[i][k]][new_list[j]]+=1
                        continue
                    else:
                        new_pair={new_list[j]:1}
                        main_dict[sentences[i][k]][new_list[j]]=1
                
            else:
                sub_dict={}
                for j in range(0,len(new_list)):
                    if new_list[j] in sub_dict:
                        sub_dict[new_list[j]]+=1
                        continue
                    else:
                        new_pair={new_list[j]:1}
                        sub_dict.update(new_pair)
                main_dict.update({sentences[i][k]:sub_dict})
    return main_dict

def split_sentences(text):
    text=text.lower()
    text=text.replace(","," ")
    text=text.replace("-"," ")
    text=text.replace(":"," ")
    text=text.replace(";"," ")
    text=text.replace("\n"," ")
    text=text.replace("\\u"," ")
    return text

def build_semantic_descriptors_from_files(filenames):
    main_dict={}
    actual_list=[]
    for i in range(len(filenames)):
        with open(filenames[i],"r",encoding="latin1") as file:
            file_content=file.read()
        file_content=split_sentences(file_content)
        my_list=[]
        full_list=[]
        for char in file_content:
            if not char in [".","!","?",",","''"]:
                my_list.append(char)
            elif char in [".","!","?",","]:
                full_list.append(''.join(my_list).strip())
                my_list=[]
        
        for i in range(len(full_list)):
            actual_list.append(full_list[i].split())
    update_dict=build_semantic_descriptors(actual_list)
    main_dict.update(update_dict)
    return main_dict

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    maxsimilarity=0
    maxchoiceindex=0
    worddict=semantic_descriptors[word]
    for i in range(len(choices)):
        choicedict=semantic_descriptors[choices[i]]
        similarityval=similarity_fn(worddict,choicedict)
        if similarityval>maxsimilarity:
            maxsimilarity=similarityval 
            maxchoiceindex=i
    return choices[maxchoiceindex]

        


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    with open(filename,'r',encoding='latin1') as file:
        lines=file.readlines()
    correct_guess=0
    attempt=0
    for line in lines:
        words=line.split()
        word=words[0]
        correct_ans=words[1]
        choices=[]
        for i in range(2,len(words)):
            choices.append(words[i])
        guess=most_similar_word(word,choices,semantic_descriptors,similarity_fn)
        if guess==correct_ans:
            correct_guess+=1
        attempt+=1
    return (correct_guess/attempt)*100

