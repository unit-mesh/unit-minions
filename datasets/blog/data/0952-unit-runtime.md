# Unit Runtime：一键运行 AI 生成的代码，或许将成为你的复制 + 粘贴神器

在我们构建了 Unit Mesh 架构之后，以及对应的 demo 之后，便着手于实现 Unit Mesh 架构。于是，我们就继续开始 Unit Runtime，以用于直接运行 AI 生成的代码。

PS：再重新介绍一下 Unit，这里的 Unit 指的是由 **AI 生成的 + 可独立运行的代码单元**，比如一个前端组件、一个 完整的 API （Controller-Service-Repository）等等。

先上链接：[https://github.com/prompt-engineering/unit-runtime](https://github.com/prompt-engineering/unit-runtime)

## 为什么我们需要 Unit Runtime？

简单来说，就是直接 AI 生成代码会遇到一系列问题：

- 无法直接运行。生成的代码多数只是一个片段，没有完整的环境，如依赖等等。
- 可调试性差：在某些情况下，AI 生成的代码可能难以调试和测试，因为人们可能难以追踪代码中的错误和逻辑错误。
- 基础设施问题：那些非业务相关的部分，诸如 HTTP 端口、数据库访问，等等。
- 现有解决方案的限制：目前，AI 生成代码的主要解决方案是使用 REPL，但它存在一些限制，如缺乏代码编辑和保存功能以及限制支持的编程语言和框架。

因此，需要开发更多的解决方案来解决这些问题。理想情况下，这个环境应该提供以下的功能：

- 环境隔离：为每个 Unit 提供独立的运行环境，使得多个 Unit 可以在同一个进程中同时运行，互不干扰。
- 依赖管理：通过自动化的依赖分析和管理，使得开发者不需要手动安装和管理依赖。
- 调试支持：通过提供交互式的控制台，使得开发者可以方便地进行调试和测试。
- 基础设施支持：提供了对 HTTP 端口、数据库访问等基础设施的支持，使得开发者可以更加方便地编写和运行业务代码。

简单来说，它应该提供一种更加便捷、高效和可靠的方式来运行 AI 生成的代码，同时也提供了更加友好和易用的工具和基础设施。

## Unit Runtime，一个 AI 生成代码运行环境

如我们在 GitHub 上所介绍：Unit Runtime 是一个 ChatGPT 等 AI 代码的运行环境，可一键启动并实时交互，帮助您快速构建和测试 AI 代码。

### Unit Runtime 处理过程

如 README 所介绍，下图是基于 Unit Runtime 运行代码的完整过程：

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/98b7da3a-98e4-4ee5-90d9-71f547fd4c6f/Untitled.png)

整个过程可以理解为一个迭代的过程，人类提供的提示被用来生成代码，代码被提交给 Unit Runtime 进行编译和执行，结果被返回给 LLM/ChatGPT 进行处理和展示，人类对结果进行验证和修改，然后再次提交给 Unit Runtime 进行编译和执行，如此循环迭代直至达到预期的结果。

而其中的 Unit Runtime 提供了一个方便的运行环境，使得代码的编译和执行更加高效、可靠和方便。

### Unit Runtime 的特性

在有了上面的内容之后，我们就可以让 ChatGPT 帮我们总结一下 Unit Runtime 的一些特性。

- **多语言支持**：支持 TypeScript、Kotlin、JavaScript、Rust 等语言，使得用户可以使用不同的编程语言来编写 AI 生成的代码片段，从而提高了灵活性和可用性。
- **Web 开发框架支持**：支持 Spring、Ktor、React 等 Web 开发框架，这使得用户可以使用不同的 Web 开发框架来构建他们的应用程序，并将 AI 生成的代码片段集成到这些应用程序中。
- **基础设施集成**：Unit Runtime 提供了对常见基础设施的支持，例如数据库、HTTP 端口等等，这些基础设施可以在编写 AI 生成的代码片段时被直接使用，从而减少了编写和维护这些代码的复杂性。
- **依赖管理**：Unit Runtime 支持依赖管理，可以自动处理依赖项并将其添加到代码中。这大大简化了开发人员的工作，使他们可以专注于代码的实现，而不是处理依赖项的安装和管理。
- **部署灵活性**：Unit Runtime 的代码可以轻松部署到不同的环境中，包括本地环境、云环境等等。这使得开发人员可以根据他们的需要选择最适合他们的部署方案。
- **可扩展性**：Unit Runtime 是可扩展的，可以轻松地添加新的语言支持、框架支持和其他功能。这使得开发人员可以使用最新的技术和工具来扩展他们的应用程序。

当然了，这不都是基本的废话吗？

## Unit Runtime 如何工作

当前版本的 Unit Runtime，每个语言都是独立的，我们正在自由的实现各种好玩的 runtime。所以，暂时没有考虑怎么去做个胶水层，唯一一样的是：

1. 使用统一的 WebSocket 方式：`ws://localhost:8080/repl`
2. 统一的输入和输出

随后，在 ChatFlow + React 的基础上写一个渲染层，它会：

1. 连接 WebSocket 服务
2. 在用户点击的时候，发送对应的代码
3. 根据返回的类型，使用不同的方式展示。如普通的 REPL 返回结果，Spring 返回 API 地址等等。

总的来说，这个过程蛮简单的。

### 一个 React 的 Hello, World 示例

如下是一个 React 生成的 Hello, World：

```tsx
import React, {useState, useEffect} from "react";
import ReactDom, {createRoot} from "react-dom/client";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<h1>Hello, world!</h1>);
```

在启动了对应的 Runtime 之后，只需要点击 Run 就会返回结果：

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/a9295418-0b4a-4289-a678-906aafd687af/Untitled.png)

至于是如何跑出结果，大家可以自己去看代码：[https://github.com/prompt-engineering/unit-runtime](https://github.com/prompt-engineering/unit-runtime)

### 一个 Spring 示例

相似大家又看过之前的 Unit Mesh 介绍了，如下是对应的 Kotlin + Spring 示例代码：

```kotlin
%use spring, kotless

@RestController
class SampleController {
  @GetMapping("/hello")
  fun helloKotlin(): String {
    return "hello world"
  }
}
```

同样的，也是一键运行。

## 未来：从 MathPrompter 看 AI 编程如何靠谱

我们构建 Unit Runtime 的另外一个动力是源自于 MathPrompter，也就是那一篇微软的论文：《**MathPrompter: Mathematical Reasoning using Large Language Models**》

> MathPrompter 是一个利用 chain-of-thought（CoT）提示技术提高大型语言模型（LLMs）在数学推理问题上表现的方法。它通过生成代数模板，提供多个数学提示并对其进行统计显著性测试来验证分析解决方案，从而增加对其生成答案的信心。
> 

在我们有了 Unit Runtime 之后，我们也可以用相似的方式构建 CodePrompter / UnitPrompter。所以，如果你也有兴趣，欢迎来挖坑。

Unit Runtime 地址：[https://github.com/prompt-engineering/unit-runtime](https://github.com/prompt-engineering/unit-runtime)
