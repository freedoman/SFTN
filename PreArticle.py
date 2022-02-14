import os
import re


def PreArticle():
    articleDirName = ""
    if os.path.exists("data"):
        filePattern = re.compile('^[^.].*?$', re.S | re.IGNORECASE)
        articleDirName = [f for f in os.listdir("data") if re.match(filePattern, f)][0]
        articleDirPath = '{0}/{1}'.format('data', articleDirName)
        articleList = [f for f in os.listdir(articleDirPath) if re.match(filePattern, f)]
        articleList.sort()

        articlePattern = getArticlePattern(articleList)
        articlePreList = getArticlePrepared(articleList, articlePattern, articleDirPath)
        return articleDirName, articlePreList

    else:
        return None

def getArticlePattern(articleList):
    metaPattern = re.compile('(\w{2}|\w{4}|[\u4e00-\u9fa5]{3}).*?', re.S)
    # print(articleList)
    articleInfo = [re.match(metaPattern, article).group(1) for article in articleList]
    articleInfo = list(set(articleInfo))
    articleInfo.sort()
    # print(articleInfo)
    articlePattern = [(re.compile('^(' + info + '.*?)\d*\.(jpg|png|pdf)$', re.S | re.IGNORECASE), re.compile('^(' + info + '.*?)\.(mp3|m4a)$', re.S | re.IGNORECASE)) for info in articleInfo]
    return articlePattern    

def deleteSpecialCharacter(astring):
    specialCharacter = '&'
    for s in specialCharacter:
        astring = re.sub(s,'',astring)
    return astring.strip()

def getArticlePrepared(articleList, articlePattern, articleDirPath):
    articlePreList = {}
    for pattern in articlePattern:
        # print(pattern)
        articleName = ""
        articleItem = {}
        articleText = set()
        artcileWav = set()
        for article in articleList:
            resText = re.match(pattern[0], article)
            if resText:
                if not articleName:
                    articleName = resText.group(1)
                # print("articleName before: ", articleName)
                articleName = deleteSpecialCharacter(articleName)
                # print("articleName after: ", articleName)
                articleText.add('{0}/{1}'.format(articleDirPath, article))
            else:
                resWav = re.match(pattern[1], article)
                if resWav:
                    if not articleName:
                        articleName = resWav.group(1)
                    artcileWav.add('{0}/{1}'.format(articleDirPath, article))
        articleItem.update({"text": articleText, "wav": artcileWav})
        articlePreList.update({ articleName: articleItem})
        # print(artcileWav)
        # print()
    # print(articlePreList)
    return articlePreList

if __name__ == '__main__':
    data = PreArticle()
    print(data)

# articlePreList
# {
#     "first artcile name":
#     {
#         "text":
#         {

#         }
#         "wav":
#         {

#         }
#     }
# }



























