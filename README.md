# 《AI 研发提效研究：自己动手训练 LoRA》 

Unit Minions 旨在训练 Unit Mesh 所需要的一系列 LoRA，由于过程数据复杂，便顺便编写了这个指南。

## Introduction

LLaMA 系列在线视频：

- 《[自制 AI 编程 Lora：手把手教会 Alpaca 编写测试代码](https://www.bilibili.com/video/BV1jg4y1G7Xc/)》
- 《[自制 AI 编程助手：自定义数据集 + 开源大模型 LLaMA + LoRA 训练](https://www.bilibili.com/video/BV1Rh411u74H/)》
- 《[自己动手训练个 AI 产品经理：手把手教会 LLaMA 编写详细需求](https://www.bilibili.com/video/BV1Us4y1N7rd/)》

ChatGLM 系列在线视频：

- TODOs

### Roadmap

Roadmap：

- 训练 1：测试代码生成
- 训练 2：生成用户故事
- 训练 3：生成代码
- 训练 4：SQL 转换
- 训练 5：生成 API 代码（设计中）
- 训练 6：……
- 训练 7：生成 Unit Mesh 的代码块

### Sponsors

Thanks: [AIOS Club](https://github.com/aios-chat) for OpenAI Key, Thanks [OpenBayes](https://openbayes.com/console/signup?r=phodal_uVxU) for Cloud GPU

<a href="https://github.com/gzzengwei"><img src="https://avatars.githubusercontent.com/u/656662?s=70&v=4" width="30px" alt="gzzengwei" /></a>
<a href="https://github.com/trampboy"><img src="https://avatars.githubusercontent.com/u/2819756?s=70&v=4" width="30px" alt="trampboy" /></a>
<a href="https://github.com/daochouwangu"><img src="https://avatars.githubusercontent.com/u/4903149?s=120&v=4" width="30px" alt="daochouwangu" /></a>
<a href="https://github.com/xuzongbao"><img src="https://avatars.githubusercontent.com/u/12446449?s=70&v=4" width="30px" alt="xuzongbao" /></a>
<a href="https://github.com/stevenchendan"><img src="https://avatars.githubusercontent.com/u/30310671?s=70&v=4" width="30px" alt="stevenchendan" /></a>
<a href="https://github.com/coderprepares"><img src="https://avatars.githubusercontent.com/u/66911083?s=64&v=4" width="30px" alt="coderprepares" /></a>
<a href="https://github.com/go-maple"><img src="https://avatars.githubusercontent.com/u/97354215?s=64&v=4" width="30px" alt="go-maple" /></a>
<a href="https://github.com/aios-chat"><img src="https://avatars.githubusercontent.com/u/126129567?v=4" width="30px" alt="aios-chat" /></a>

PS：训练烧钱……（调用 OpenAI 生成数据（仅限于需求细化）、云 GPU），如果你觉得帮到你，可以通过以下方式，帮助我们继续往前。

<table>
  <tr>
    <td><img src="images/alipay.pic.jpg"  alt="1" width = 240px  ></td>
    <td><img src="images/zsxq.pic.jpg" alt="2" width = 240px ></td>
  </tr>
</table>

用支付宝的同学记得注明你的 GitHub id。

# 基于 Meta 的 Llama 训练 LoRA

相关背景：

1. 基础模型：Meta 开源 LLaMA 系列模型
2. Instruct-Tune：[https://github.com/tloen/alpaca-lora](https://github.com/tloen/alpaca-lora)

由于，我们的目标不是对模型调优、生成通用的模型，而是训练特定用途的 Lora。因此，我们没有加入：[Stanford Alpaca](https://github.com/tatsu-lab/stanford_alpaca) 中的数据，
故所需要时间更短，如 8000+ 测试代码只需要 1 小时，3400+ 的用户故事只需要 25 分钟。

训练步骤见：

- 方式 1：直接使用：[alpaca-lora.ipynb](alpaca-lora.ipynb) 
- 方式 2：直接使用：[OpenBayes 容器](https://openbayes.com/console/phodal/containers/JBx5YD7HTdS) （PS：使用我的专用邀请链接，注册 OpenBayes，双方各获得 60 分钟 RTX 3090 使用时长，支持累积，永久有效：
https://openbayes.com/console/signup?r=phodal_uVxU) ）

## 训练 1：根据业务代码生成测试代码

代码生成测试用例的 Lora 见：[https://github.com/unit-mesh/unit-minions/releases/tag/v0.0.1](https://github.com/unit-mesh/unit-minions/releases/tag/v0.0.1)

![](images/test-process.jpeg)

基本思路：

- 在时间有限的情况下，基于 OpenAI 的数据来完善。但是，OpenAI 编写的测试用例不一定靠谱，所以让他生成业务代码。
- 在时间充裕的情况下，可以分析 AST 来合并第一和第二步，也是比较合理的方案，毕竟 OpenAI 的 API 很贵。

### 步骤 1. 准备数据

1. 下载 GitHub 上的项目（需要包含测试用例）
2. 建立每个项目的 `src/main` 下的 Java 文件 map，如果同时存在对应的测试文件，则拉入的数据集中。
3. 并生成每个测试对应的类的基本信息（以减少 OpenAI Token 使用）：
```
org.unitmesh.processor.TestClass(String, Int)
- fields: field1:String, field2:Int
- methods: method1(String, Int): String, method2(): Int
```
4. 按测试用例（即 @Test 方法）拆分每个测试文件，拆成 N 个（即 test1、test2 是两个不同的数据）
```java
class TestProcessorTest {
    @Test
    void test1() {
    }
    
    @Test
    void test2() {
    }
}
```

最后，生成的数据如下：

{"classInfo": "com.thoughtworks.go.security.AESEncrypter(AESCipherProvider)\n- fields: ENCODER:Base64.Encoder, DECODER:Base64.Decoder, cipherProvider:AESCipherProvider, ivProvider:IVProvider\n- methods: createIVProviderInstance(): IVProvider, canDecrypt(String): boolean, encrypt(String): String, decrypt(String): String, createSecretKeySpec(): SecretKeySpec", "testMethod": "public class AESEncrypterTest {\n\n    private AESEncrypter aesEncrypter;\n\n    @Test\n    public void shouldGenerateEncryptedText() throws CryptoException {\n        String encrypt = aesEncrypter.encrypt(\"p@ssw0rd\");\n        assertThat(encrypt).startsWith(\"AES\");\n        assertThat(encrypt.split(\":\")).hasSize(3);\n    }\n}\n", "id": "task_0"}

### 步骤 2. 使用 OpenAI Davinci 编写实现代码（代码见：[test-to-code.py](code/test-to-code.py)）


1. 将上面的数据转换为 JSONL，合并成 prompt。
2. 让 Davinci 完成填空题。

最后生成的 prompt 示例如下：

```markdown
You are a programmer and implementation a method with TDD. Here are the requirements:

1. According follows class information and tests code to write a method.
2. Try you best to thinking corner case.
3. You only return the code, no explain.

class information: 

### 
io.github.robwin.swagger.test.AbstractContractValidator()
- methods: findExpectedPaths(Swagger, SwaggerAssertionConfig): Map<String,Path>, getPathsIncludingBasePath(Swagger): Map<String,Path>, getPathsWithPrefix(Swagger, String): Map<String,Path>, isBlankOrSlash(String): boolean
###

test code: 

### 
/**
 * Tests AbstractContractValidator.
 */
@RunWith(Enclosed.class)
public class AbstractContractValidatorTest {

    /**
     * Tests getPathsIncludingBasePath().
     */
    public static class GetPathsIncludingBasePath {

        @Test
        public void shouldReturnPathsPrefixedIfBasePathSet() {
            // given
            Swagger swagger = buildSwaggerFrom("/swagger.json");
            // when
            Map<String, Path> paths = new DummyValidator().getPathsIncludingBasePath(swagger);
            // then
            paths.entrySet().forEach(e -> assertThat(e.getKey(), startsWith(swagger.getBasePath())));
        }
    }

    /**
     * Tests findExpectedPaths().
     */
    public static class FindExpectedPaths {
    }

    private static class DummyValidator extends AbstractContractValidator {
    }
}
###

```

### 步骤 3. 训练

训练步骤可以直接使用： [alpaca-lora.ipynb](alpaca-lora.ipynb)

### 示例输出

```

```

## 训练 2：拆分用户故事

训练步骤可以直接使用： [alpaca-lora.ipynb](alpaca-lora.ipynb) 或者直接使用 OpenBayes 容器：https://openbayes.com/console/phodal/containers/JBx5YD7HTdS

代码生成测试用例的 Lora 见：[https://github.com/unit-mesh/unit-minions/releases/tag/v0.0.2](https://github.com/unit-mesh/unit-minions/releases/tag/v0.0.2)

结果：

![User Story 结果](images/alpaca-user-story-training.jpg)


基本思路：

1. 结合常见的领域（如在线网站），借用 OpenAI 生成用户任务（如登录、浏览列表等等）
2. 根据用户故事生成用户故事。
3. 训练 Alpaca LoRA。

如下所示：

![](images/alpaca-user-story-lora.jpeg)

### 步骤 1. 准备数据

1. 调用 OpenAI 按分类创建用户任务。prompt 如下：

```markdown
Design a User Story Mapping for ${domain} application based on your understanding. Here are the requirements: 

1. Your user story map should include only user tasks to demonstrate how users will interact with the application.
2. Our user story map should be based on your understanding of the ${domain} application and its users, and should be designed to address their needs and pain points.
3. You may use any tools or formats you choose to create your user story map, but it should be easily shareable and understandable by stakeholders.
4. Your expression should be more concise and clear.
5. Your return should be like as follows:

###
User Tasks:
1. ...
###
```

2. 调用 OpenAI 根据用户任务创建用户故事。prompt 如下：

```markdown
为下面的需求编写用户故事：${domain} 应用的 ${story_name} 功能。 要求如下：

1. 必须要考虑尽可能考虑各种异常场景，添加更多的 AC。
2. 你的返回模板如下所示：

###
用户故事：可以选择宝贝出行服务
作为 莉莉妈
我想 在滴滴打车的手机客户端里选择宝贝出行服务
以便于 我能够带宝宝打车出行的时候打到有儿童座椅的车

AC 1:  莉莉妈可以选择宝贝出行服务
假设 xxx
当 xxx
于是 xxx
###
```

### 步骤 2. 训练

训练步骤可以直接使用： [alpaca-lora.ipynb](alpaca-lora.ipynb)

### 示例输出

```
print(evaluate("create Agile user story for following topic: ", "购买电影票", 0.1, 0.75, 40, 4, 512))

用户故事：可以购买电影票
作为一个电影票购买者
我想在购买电影票应用中购买电影票
以便于我可以购买电影票
AC 1: 电影票购买者可以在购买电影票应用中购买电影票
假设 电影票购买者已经登录购买电影票应用
当 电影票购买者点击“购买电影票”按钮
于是 电影票购买者可以在购买电影票应用中购买电影票
AC 2: 电影票购买者可以在购买电影票应用中查看购买记录
假设 电影票购买者已经登录购买电影票应用
当 电影票购买者点击“查看购买记录”按钮
于是 电影票购买者可以在购买电影票应用中查看购买记录
AC 3: 电影票购买者可以在购买电影票应用中查看购买记录
假设 电影票购买者已经登录购买电影票应用
当 电影票购买者点击“查看购买记录”按��
```

## 训练 3：代码辅助

训练结果 Lora 见：https://github.com/unit-mesh/unit-minions/releases/tag/v0.0.3

思路：

![Copilot Element](images/copilot-elements.png)

### 步骤 1. 准备数据

1. 下载 GitHub 上的项目（需要包含测试用例）
2. 遍历 `src/main` 下的 Java 文件。
3. 生成每个类的基本信息：
```
PostService(PostRepository, UserRepository, ImageService)
- fields: postRepository:PostRepository, userRepository:UserRepository, userPosts:Set<Post>, imageService:ImageService
- methods: findAll(): List<Post>, addNewPost(Post): Post, saveImageToPost(String, MultipartFile, Post): int
```
4. 生成 instruct

格式：

- instruction: Implement the method ${methodName}
- input: ${classInformation}
- output: ${code}

示例：

```
{"instruction":"Implement the method action","input":"com.thoughtworks.go.config.rules.AbstractDirective(DirectiveType, DirectiveType, String, String, String)\n- fields: action:String, type:String, resource:String, configErrors:ConfigErrors, directiveType:DirectiveType\n- methods: validate(ValidationContext): void, isInvalid(String, List<String>): boolean, matchesAction(String): boolean, matchesType(Class<? extends Validatable>): boolean, matchesResource(String): boolean, errors(): ConfigErrors, addError(String, String): void, equals(Object): boolean, action(): String, type(): String, resource(): String, hashCode(): int, hasErrors(): boolean, getDirectiveType(): DirectiveType","output":"public abstract class AbstractDirective implements Directive {\n\n    @ConfigAttribute(value = \"action\", optional = false)\n    protected String action;\n\n    @ConfigAttribute(value = \"type\", optional = false)\n    protected String type;\n\n    @ConfigValue\n    private String resource;\n\n    private final ConfigErrors configErrors = new ConfigErrors();\n\n    private DirectiveType directiveType;\n\n    public AbstractDirective(DirectiveType allow) {\n        this.directiveType = allow;\n    }\n\n    public AbstractDirective(DirectiveType allow, String action, String type, String resource) {\n        this.directiveType = allow;\n        this.action = action;\n        this.type = type;\n        this.resource = resource;\n    }\n\n    @Override\n    public String action() {\n        return this.action;\n    }\n}\n"}
```

### 类信息格式

格式规范：

```
包名.类名(类的构造类型)
- fields：成员变量集合（变量名:类型）
- methods：方法抽象集合（方法名(参数类型): 输出类型）
```

结果：

```
com.thoughtworks.go.config.rules.AbstractDirective(DirectiveType, DirectiveType, String, String, String)
- fields: action:String, type:String, resource:String, configErrors:ConfigErrors, directiveType:DirectiveType
- methods: validate(ValidationContext): void, isInvalid(String, List<String>): boolean, matchesAction(String): boolean, matchesType(Class<? extends Validatable>): boolean, matchesResource(String): boolean, errors(): ConfigErrors, addError(String, String): void, equals(Object): boolean, action(): String, type(): String, resource(): String, hashCode(): int, hasErrors(): boolean, getDirectiveType(): DirectiveType
```

### 核心代码逻辑

```kotlin
val javaProcessor = JavaProcessor(file.readText())
val shotClass = javaProcessor.toShortClass() ?: return@forEach

javaProcessor
   .removePackage()
   .removeAllImport()
   .removeLicenseInfoBeforeImport()

javaProcessor.splitMethods().forEach { (key, value) ->
   CodegenPrompt(
       instruction = "Implement the method $key",
       input = shotClass.toString(),
       output = value
   ).let { prompt ->
       val output = Json.encodeToString(prompt)
       File("$targetPath${key}.json").writeText(output)
   }
}
```

### 步骤 2. 训练

训练步骤可以直接使用： [alpaca-lora.ipynb](alpaca-lora.ipynb)

### 示例输出

```
print(evaluate("Implement the method rmFiles", "FileUtils:", 0.1, 0.75, 40, 4, 512))

public class FileUtils {

    private FileUtils() {
    }

    public static void rmFiles(String path) {
        File dir = new File(path);
        File[] files = dir.listFiles();
        if (files != null) {
            for (File file : files) {
                if (file.isFile()) {
                    file.delete();
                } else if (file.isDirectory()) {
                    FileUtils.rmFiles(file.getAbsolutePath());
                }
            }
        }
    }
}
```
