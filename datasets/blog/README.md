原理：

- 首先准备好文档，并整理为纯文本的格式。
- 把每个文档切成若干个小的 chunks 调用文本转向量的接口，将每个 chunk 转为一个向量，并存入向量数据库
   - 文本转向量可以使用 OpenAI embedding（https://platform.openai.com/docs/guides/embeddings/what-are-embeddings） 也可以使用其他方案，如 fasttext/simbert 等
- 当用户发来一个问题的时候，将问题同样转为向量，并检索向量数据库，得到相关性最高的一个或几个 chunk
- 将问题和chunk合并重写为一个新的请求发给 OpenAI api，可能的请求格式如下：

```
结合下面的段落来回答问题：“ 如何使用预约功能”

* 段落1: 您可以按照以下步骤使用预约功能....
* 段落2: 在使用预约功能之前，请确保您已正确地设置了洗涤程序....
* 段落3: .......
```


 