## 安卓一键打渠道包工具


#### 实现原理

![](https://github.com/ikool-cn/Android-channel-build-tool/blob/master/Screenshot.png)

写入一个空文件channel_{name}到安卓apk的META-INF目录下,然后安卓读取channel_{name}匹配出渠道名称。注意apk打包的时候需要采用v1签名，这样修改后的apk包不用重签名。
测试速度每分钟可以打几百上千个包，视磁盘速度和apk大小而定。

如果v2签名的话修改包后得重签名。
