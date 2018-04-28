- 更新bilibili直播间自动领便当脚本

- Mht格式QQ聊天记录转Html格式

- 自动评教脚本

- 七牛云自动上传脚本 win10 py2 py3,mac py2

  ​

  ​


## 修改python2的默认编码

python2的默认编码是ascii,当程序中出现非ascii编码时，python的处理常常会报这样的错:

UnicodeDecodeError: ‘ascii’ codec can’t decode byte 0x?? in position 1: ordinal not in range(128)

python没办法处理非ascii编码的，此时需要自己设置将python的默认编码，一般设置为utf8的编码格式。

解决方案：在路径`/Library/Python/2.7/site-packages`[下新建一个sitecustomize.py](http://xn--sitecustomize-9z0u6ewtg47usiza.py/)，内容为：

```
# encoding=utf8  
import sys  
  
reload(sys)  
sys.setdefaultencoding('utf8')  

```

这个时候重启python解释器，执行sys.getdefaultencoding()，会发现此时的默认编码已经转换成utf-8了，多次重启之后，效果相同，这是因为系统在python启动的时候，自行调用该文件，设置系统的默认编码，而不需要每次都手动的加上解决代码，属于一劳永逸的解决方法。