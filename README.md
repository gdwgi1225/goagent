DON'T PANIC

  * page  [gdwgi1225-goagent](http://gdwgi1225-hrd.appspot.com/page/gdwgi1225-goagent)
  * api   [gdwgi1225-goagent](http://gdwgi1225-hrd.appspot.com/api/gdwgi1225-goagent)

## 简易教程

- 部署

  1. 申请 Google Appengine 并创建 appid。
  2. 下载 goagent 最新版 https://github.com/goagent/goagent
  3. 修改 proxy.ini 中的 [gae] 下的 appid = 你的appid(多appid请用|隔开)
  4. 运行 uploader.bat 或 uploader.py 开始上传, 成功后即可使用了。

- 使用

  * Windows 用户推荐使用 goagent.exe 托盘图标设置 IE 代理(对其它浏览器也有效)。
  * Chrome/Opera 请安装 [SwitchySharp](https://chrome.google.com/webstore/detail/dpplabbmogkhghncfbfdeeokoefdjegm) 插件（拖放  SwitchySharp.crx 到扩展设置），然后导入 SwitchyOptions.bak
  * Firefox 请安装 [FoxyProxy](https://addons.mozilla.org/zh-cn/firefox/addon/foxyproxy-standard/) ，Firefox需要导入证书，方法请见 FAQ
  * 出现连接不上的情况可以尝试使用 [GoGo Tester](https://github.com/azzvx/gogotester/raw/master/GoGo%20Tester/bin/Debug/GoGo%20Tester.exe) 测速。

## 最近更新
* [1122 否] 3.2.3 正式版，修复 MacOSX/Linux 平台 CPU 100% 的问题；托盘图标支持设置ADSL拨号网络代理(注意：拨号网络请使用英文名称）。

## 讨论区
* https://code.google.com/p/goagent/issues/list

## 文档
* 简易教程 https://github.com/goagent/goagent/blob/wiki/SimpleGuide.md
* 图文教程 https://github.com/goagent/goagent/blob/wiki/InstallGuide.md
* 常见问题 https://github.com/goagent/goagent/blob/wiki/FAQ.md
* 配置介绍 https://github.com/goagent/goagent/blob/wiki/ConfigIntroduce.md
* 五毛观止 https://github.com/goagent/goagent/blob/wiki/SpamList.md
* 更新历史 https://github.com/goagent/goagent/blob/wiki/History.md

## 代码
 * proxy.py      https://github.com/goagent/goagent
 * python27.exe  https://github.com/goagent/pybuild
 * goagent.exe   https://github.com/goagent/taskbar