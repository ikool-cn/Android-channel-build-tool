## 安卓一键打渠道包工具


#### 目录结构
```bash
|---Java #安卓读取channel类
|---Python #打包工具
```

![](https://github.com/ikool-cn/Android-channel-build-tool/blob/master/Screenshot.png.png)

### 实现原理
 - 写入一个空文件channel_xxx到安卓apk的META-INF目录下
 - 安卓读取META-INF目录下的channel_xxx文件匹配出渠道名称
 - 注意apk打包的时候务必采用V1签名，这样修改后的apk包不用重签名

### APK Signature Scheme v2
    目前安卓没有强制要求使用V2签名，所以上面的方法足以满足我们的需求，假如以后强制使用V2签名的话也有解决方案。
    Android 7.0（Nougat）推出了新的应用签名方案APK Signature Scheme v2后，我们看一下zip文件结构。

![](https://github.com/ikool-cn/Android-channel-build-tool/blob/master/v2.png)

新应用签名方案的签名信息会被保存在区块2（APK Signing Block）中， 而区块1（Contents of ZIP entries）、区块3（ZIP Central Directory）、区块4（ZIP End of Central Directory）是受保护的，在签名后任何对区块1、3、4的修改都逃不过新的应用签名方案的检查。

之前的渠道包生成方案是通过在META-INF目录下添加空文件，用空文件的名称来作为渠道的唯一标识，之前在META-INF下添加文件是不需要重新签名应用的，这样会节省不少打包的时间，从而提高打渠道包的速度。但在新的应用签名方案下META-INF已经被列入了保护区了，向META-INF添加空文件的方案会对区块1、3、4都会有影响，新应用签名方案签署的应用经过我们旧的生成渠道包方案处理后，在安装时会报错。

通过上面的描述，可以看出因为APK包的区块1、3、4都是受保护的，任何修改在签名后对它们的修改，都会在安装过程中被签名校验检测失败，而区块2（APK Signing Block）是不受签名校验规则保护的，那是否可以在这个不受签名保护的区块2（APK Signing Block）上做文章呢？我们先来看看对区块2格式的描述：

![](https://github.com/ikool-cn/Android-channel-build-tool/blob/master/v2.png)

区块2中APK Signing Block是由这几部分组成：2个用来标示这个区块长度的8字节 ＋ 这个区块的魔数（APK Sig Block 42）+ 这个区块所承载的数据（ID-value）。

我们重点来看一下这个ID-value，它由一个8字节的长度标示＋4字节的ID＋它的负载组成。V2的签名信息是以ID（0x7109871a）的ID-value来保存在这个区块中，不知大家有没有注意这是一组ID-value，也就是说它是可以有若干个这样的ID-value来组成，那我们是不是可以在这里做一些文章呢？

通过源代码可以看出Android是通过查找ID为 APK_SIGNATURE_SCHEME_V2_BLOCK_ID = 0x7109871a 的ID-value，来获取APK Signature Scheme v2 Block，对这个区块中其他的ID-value选择了忽略。

在APK Signature Scheme v2中没有看到对无法识别的ID，有相关处理的介绍。

当看到这里时，我们可不可以设想一下，提供一个自定义的ID-value并写入该区域，从而为快速生成渠道包服务呢？