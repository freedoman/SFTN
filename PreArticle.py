import os
import re


def PreArticle():
    articleDirName = ""
    if os.path.exists("data"):
        articleDirName = os.listdir("data")[1]
        articleDirPath = '{0}/{1}'.format('data', articleDirName)

        filePattern = re.compile('^[^.].*?$', re.S | re.IGNORECASE)
        articleList = [f for f in os.listdir(articleDirPath) if re.match(filePattern, f)]
        articleList.sort()

        articlePattern = getArticlePattern(articleList)
        articlePreList = getArticlePrepared(articleList, articlePattern, articleDirPath)
        return articlePreList

    else:
        return None

def getArticlePattern(articleList):
    metaPattern = re.compile('(\d{2}|[\u4e00-\u9fa5]{3}).*?', re.S)
    print(articleList)
    articleInfo = [re.match(metaPattern, article).group(1) for article in articleList]
    articleInfo = list(set(articleInfo))
    articleInfo.sort()
    articlePattern = [(re.compile('^(' + info + '.*?)\d*\.(jpg|png|pdf)$', re.S | re.IGNORECASE), re.compile('^(' + info + '.*?)\.(mp3|m4a)$', re.S | re.IGNORECASE)) for info in articleInfo]
    return articlePattern    



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
                # print("articleName: ", articleName)
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



























