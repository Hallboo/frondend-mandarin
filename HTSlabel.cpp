#include <iostream>
#include <vector>
using namespace std;
bool debug=0;

class LabNode{
public:
    LabNode *lbrother=NULL;
    LabNode *rbrother=NULL;
    LabNode *father=NULL;
    vector<LabNode *> sons;
    int sons_number=0;
    int rhythm;
    string pose;
    string content;//stentence，phrase，syllable，phone
};

class HTSlabel{
private:
    LabNode * root;//tree root node
    LabNode * fphone;//first phone node
    int FindMax(vector<int> &seq);
    int FindMin(vector<int> &seq);
    bool treePerLeaf(LabNode * p,vector<string> word,int level);
    bool treePerLevel(LabNode * p, vector<string> words, vector<int> rhythms, vector<vector<vector<string>>> syllables, int level);
public:
    LabNode* Tree(vector<string> words, vector<int> rhythms, vector<vector<vector<string>>> syllables, vector<string> poses, vector<string> phs_type);
    void ShowTree(LabNode *p);
    bool LabGenerator(LabNode *fphone);
};
//-------------------------------------------------------------------------------------------------------------------
int HTSlabel::FindMax(vector<int> &seq)
{
    int max=seq[0];
    for(unsigned int i=0;i<seq.size();i++)
        if(seq[i]>max)max=seq[i];
    return max;
}

int HTSlabel::FindMin(vector<int> &seq)
{
    int min=seq[0];
    for(unsigned int i=0;i<seq.size();i++)
        if(seq[i]<min)min=seq[i];
    return min;
}

bool HTSlabel::treePerLeaf(LabNode * p,vector<string> word,int level)
{
    if(--level==-2)
    {
        for(vector<string>::iterator it=word.begin();it!=word.end();it++)
            {
                LabNode * q = new LabNode;
                p->sons.push_back(q);p->sons_number++;
                q->rhythm=level;q->father=p;q->content=*it;
                if(debug)cout << "level: " << level << " q->content:" << q->content << endl; 
            }
    }else return 1;
    return 0;
}

bool HTSlabel::treePerLevel(LabNode * p, vector<string> words, vector<int> rhythms, vector<vector<vector<string>>> syllables, int level)
{
    if(words.size()!=rhythms.size() || words.size()!= syllables.size()) return 1;
    int max=FindMax(rhythms);
    int min=FindMin(rhythms);
    if(max!=min)level=max;
    else level--;
    for(unsigned int i=0,j=0;i<words.size();i++)//遍历子序列
    {
        if((rhythms[i]==level || max==min) && level>0)//if((rhythms[i]==level || 1==FindMax(rhythms)) && level>0)
        {
            if(i>j) 
            {
                vector<int> rhythmfm(rhythms.begin()+j,rhythms.begin()+i);
                rhythms[i]=FindMax(rhythmfm);
                //cout << "rhythms[i] " << rhythms[i] << endl;
            }
            else if(i==j && max==min)
                level=*rhythms.begin();
            LabNode * q = new LabNode;
            p->sons.push_back(q);p->sons_number++;
            q->rhythm=level;q->father=p;
            vector<string> subwords(words.begin()+j,words.begin()+i+1);
            vector<int> subrhythms(rhythms.begin()+j,rhythms.begin()+i+1);
            vector<vector<vector<string>>> subsyllables(syllables.begin()+j,syllables.begin()+i+1);j=i+1;
            for(unsigned int i=0;i<subwords.size();i++)
                q->content+=subwords[i];
            if(debug)//-----------------------------------------------print--------------------        
            {
                cout << "level: " << level << endl;
                cout << q->content << endl;
                for(unsigned int i=0;i<subwords.size();i++)
                    cout <<"subwords: "<< subwords[i] << " subrhythms: " << subrhythms[i] << endl;
            }//--------------------------------------------------------------------------------
            treePerLevel(q,subwords,subrhythms,subsyllables,level);
        }
        else if(max==min && level<min && level >-1)
        {
            LabNode * q = new LabNode;
            p->sons.push_back(q);p->sons_number++;
            q->rhythm=level;q->father=p;
            for(unsigned int i=0;i<words.size();i++)
                q->content+=words[i];
            if(debug)//-----------------------------------------------print--------------------        
            {
                cout << "level: " << level << endl;
                cout << q->content << endl;
                for(unsigned int i=0;i<words.size();i++)
                cout <<"subwords: "<< words[i] << " subrhythms: " << rhythms[i] << endl;
            }//--------------------------------------------------------------------------------
            treePerLevel(q,words,rhythms,syllables,level);
        }
        else if(level==-1)
        {
            for(vector<vector<string>>::iterator it=syllables.begin()->begin();it!=syllables.begin()->end();it++)
            {
                LabNode * q = new LabNode;
                p->sons.push_back(q);p->sons_number++;
                q->rhythm=level;q->father=p;for(unsigned int i=0;i<(*it).size();i++)q->content+=(*it)[i];
                if(debug)cout << "level: " << level << endl << "q->content:" << q->content << endl; 
                treePerLeaf(q,*it,level);              
            }
        }
    }
    return 0;
}

void HTSlabel::ShowTree(LabNode *p)
{
    if(p==NULL)p=root;
    for(int i=0;i<5-p->rhythm;i++) cout << "| ";
    cout << p->rhythm << " " << p->content << endl;
    for(vector<LabNode *>::iterator it=p->sons.begin();it!=p->sons.end();it++)
        ShowTree(*it);
}

LabNode* HTSlabel::Tree(vector<string> words, vector<int> rhythms, vector<vector<vector<string>>> syllables, vector<string> poses, vector<string> phs_type)
{
 
    root = new LabNode;root->rhythm=5;
    for(vector<string>::iterator it=words.begin();it!=words.end();it++)root->content+=*it;
    treePerLevel(root, words, rhythms, syllables, 4);
    LabNode *p;p=root;
    while(p->sons.size())p=p->sons[0];
    fphone=p;
    if(debug)cout << "first phone Node : " << p->content << endl;
    return fphone;
}
//-------------------------------------------------------------tree end-------------------------------------------------

bool HTSlabel::LabGenerator(LabNode *fphone)
{

    return 0;
}
//-------------------------------------------------------------generator end--------------------------------------------
int main()//test class HTSlabel code
{
    vector<string> words={"继续","把","建设","有","中国","特色","社会","主义","事业","推向","前进"};
    vector<int> rhythms={1, 1, 2, 1, 1, 3, 1, 1, 4, 1, 4};//{1, 2, 3, 2, 1, 4, 1, 2, 3, 2, 1};//
    vector<vector<vector<string>>> syllables={{{"j", "i4"},{"x", "v4"}}, {{"b", "a3"}}, {{"j", "ian4"}, {"sh", "e4"}}, {{"y", "iou3"}}, {{"zh", "ong1"}, {"g", "uo2"}}, {{"t", "e4"}, {"s", "e4"}}, {{"sh", "e4"}, {"h", "uei4"}}, {{"zh", "u3"}, {"y", "i4"}}, {{"sh", "ih4"},{"y", "ie4"}}, {{"t", "uei1"}, {"x", "iang4"}}, {{"q", "ian2"}, {"j", "in4"}}};
    vector<string> poses={"n", "n", "n", "n", "n","n", "n", "n", "n", "n", "n"};
    vector<string> phs_type={"s",  "a",  "b",  "a",  "b",  "a",  "b",  "a",  "b",  "a",  "b",  "a",  "b",  "d",  "a",  "b",  "a",  "b",  "a",  "b",  "a",  "b",  "d",  "a",  "b",  "a",  "b",  "a",  "b",  "a",  "b",  "a",  "b",  "a",  "b",  "s",  "a",  "b",  "a",  "b",  "a",  "b",  "a",  "b",  "s"};
    HTSlabel label;
    label.Tree(words,rhythms,syllables,poses,phs_type);
    label.ShowTree(NULL);
    return 0;
}