## 安卓一键打渠道包工具


#### 实现原理

![](https://github.com/ikool-cn/Android-channel-build-tool/blob/master/Screenshot.png.png)

1. 写入一个空文件channel_xxx到安卓apk的META-INF目录下,
2. 安卓读取META-INF目录下的channel_{name}文件匹配出渠道名称（参考java目录下的代码）。注意apk打包的时候需要采用v1签名，这样修改后的apk包不用重签名。
测试速度每分钟可以打几百上千个包，视磁盘速度和apk大小而定。
