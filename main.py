from app.find_keywords import retrieve_file_keywords
import sys

if __name__ == "__main__":
    base_path=sys.argv[1]
    # "C:\\Users\\LMbogo\\OneDrive - International Monetary Fund (PRD)\\All_Raw_Data_By_Source\\"
    filepaths=sys.argv[2]
    #['AIV_2000-2021\\txt','COM_Flagships\\txt','Ereview\\txt','Program_2021\\txt']
    keywords = sys.argv[3]
    return_file=sys.argv[4]
    # list(['governance', 'corruption', 'bribery'])
    get_file_keywords=retrieve_file_keywords(base_path, keywords, filepaths,return_file)
    get_file_keywords.run()
