## 1
42行clear_single_quote调用处

## 2
？

## 3
44行memcpy(buffer, crlf + 4, vlen);战溢出


## 4
```
_malloc申请空间有误，会在base64Decode中导致堆溢出
.text:0001345A                 mov     [ebp+var_40], ecx
.text:0001345D                 mov     [ebp+s1], edx
.text:00013460                 sub     esp, 0Ch
.text:00013463                 push    edi             ; unsigned int
.text:00013464                 call    _malloc
.text:00013469                 mov     esi, eax
.text:0001346B                 push    edi             ; unsigned __int8 *
.text:0001346C                 push    eax             ; unsigned int
.text:0001346D                 mov     ecx, [ebp+var_40]
.text:00013470                 push    ecx             ; char *
.text:00013471                 mov     edx, [ebp+s1]
.text:00013474                 add     edx, 4
.text:00013477                 push    edx             ; this
.text:00013478                 call    __ZN2nv12base64DecodeEPKcjPhj ; nv::base64Decode(char const*,uint,uchar *,uint)

```


5
https://github.com/Insight8991/iot/blob/main/dir859%20Command%20Execution%20Vulnerability.md
CVE-2022-46476 soapcgi_main
对url_v3 = getenv("REQUEST_URI") 获取的参数过滤不严格，
构造命令执行snprintf 将v3格式化为commandline

```
.text:00411DB0                 lui     $a2, 0x43  # 'C'
.text:00411DB4                 lw      $gp, 0x40+var_10($sp)
.text:00411DB8                 li      $a2, aShSSDShDevCons  # "sh %s/%s_%d.sh > /dev/console &"
.text:00411DBC                 addiu   $a3, $s1, (aVarRun - 0x430000)  # "/var/run"
.text:00411DC0                 addiu   $a0, $s0, (cmd_line - 0x440000)  # s
.text:00411DC4                 la      $t9, snprintf
.text:00411DC8                 li      $a1, 0x400       # maxlen
.text:00411DCC                 sw      $s2, 0x40+var_30($sp)
.text:00411DD0                 jalr    $t9 ; snprintf
.text:00411DD4                 sw      $v0, 0x40+var_2C($sp)
.text:00411DD8                 lw      $gp, 0x40+var_10($sp)
.text:00411DDC                 la      $t9, system
.text:00411DE0                 jalr    $t9 ; system
.text:00411DE4                 addiu   $a0, $s0, (cmd_line - 0x440000)  # command
.text:00411DE8                 lw      $gp, 0x40+var_10($sp)

```
## 6 
gena.php:25行

.text:004120A4                 jalr    $t9 ; snprintf

CVE-2019 17621
buf_8 ->xmldbc_ephp->FUN_0041420c ->FUN_0041372c -> socket。


也就是说spinrtf之后通过xmldbc ephp()将acStack552这个缓冲区中包含的数据发送到php。

控制shell文件

```

    fwrite(w, $shell_file,
        "#!/bin/sh\n".
        'echo "[$0] ..." > '.$upnpmsg."\n".
        "xmldbc -P ".$target_php.
            " -V INF_UID=".$inf_uid.
            " -V HDR_URL=".SECURITY_prevent_shell_inject($uri).
            " -V HDR_HOST=".SECURITY_prevent_shell_inject($host).
            " -V HDR_SID=".SECURITY_prevent_shell_inject($sid).
            " -V HDR_SEQ=0".
            " | httpc -i ".$phyinf." -d ".SECURITY_prevent_shell_inject($host)." -p TCP > ".$upnpmsg."\n"
    );
    fwrite(a, $shell_file, "rm -f ".$shell_file."\n");
}
```

## 7
challeng.c:197

copy_from_user调用的变量未枷锁

```c
while(ucmsg != NULL) {
		__get_user(ucmlen, &ucmsg->cmsg_len);
		tmp = ((ucmlen - CMSG_COMPAT_ALIGN(sizeof(*ucmsg))) +
		       CMSG_ALIGN(sizeof(struct cmsghdr)));
		kcmsg->cmsg_len = tmp;
		__get_user(kcmsg->cmsg_level, &ucmsg->cmsg_level);
		__get_user(kcmsg->cmsg_type, &ucmsg->cmsg_type);

		/* Copy over the data. */
		
		
		if(copy_from_user(CMSG_DATA(kcmsg),CMSG_COMPAT_DATA(ucmsg),(ucmlen - CMSG_COMPAT_ALIGN(sizeof(*ucmsg)))))
			goto out_free_efault;

		/* Advance. */
		kcmsg = (struct cmsghdr *)((char *)kcmsg + CMSG_ALIGN(tmp));
		ucmsg = cmsg_compat_nxthdr(kmsg, ucmsg, ucmlen);
	}
```

## 8
challenge.c:526

```c	if(copy_from_user(&fibsize, &user_srb->count,sizeof(u32))){
		dprintk((KERN_DEBUG"aacraid: Could not copy data size from user\n"));
		rcode = -EFAULT;
		goto cleanup;
	}

	if ((fibsize < (sizeof(struct user_aac_srb) - sizeof(struct user_sgentry))) ||
	    (fibsize > (dev->max_fib_size - sizeof(struct aac_fibhdr)))) {
		rcode = -EINVAL;
		goto cleanup;
	}

	user_srbcmd = kmalloc(fibsize, GFP_KERNEL);
	if (!user_srbcmd) {
		dprintk((KERN_DEBUG"aacraid: Could not make a copy of the srb\n"));
		rcode = -ENOMEM;
		goto cleanup;
	}
	if(copy_from_user(user_srbcmd, user_srb,fibsize)){
		dprintk((KERN_DEBUG"aacraid: Could not copy srb from user\n"));
		rcode = -EFAULT;
		goto cleanup;
	}
```



## 9

chall.c:331

```c
const char *jsV_nextiterator(js_State *J, js_Object *io)
{
	int k;
	if (io->type != JS_CITERATOR)
		js_typeerror(J, "not an iterator");
	while (io->u.iter.head) {
		js_Iterator *next = io->u.iter.head->next;
		const char *name = io->u.iter.head->name; //iter name
		js_free(J, io->u.iter.head); 
		io->u.iter.head = next;
		if (jsV_getproperty(J, io->u.iter.target, name))
			return name;
		if (io->u.iter.target->type == JS_CSTRING)
			if (js_isarrayindex(J, name, &k) && k < io->u.iter.target->u.s.length)
				return name;
		if (io->u.iter.target->type == JS_CARRAY && io->u.iter.target->u.a.simple)
			if (js_isarrayindex(J, name, &k) && k < io->u.iter.target->u.a.length)
				return name;
	}
	return NULL;
}
```



## 11

challenge.c 190

```
static void nf_tables_expr_destroy(const struct nft_ctx *ctx,
								   struct nft_expr *expr)
{
	const struct nft_expr_type *type = expr->ops->type;

	if (expr->ops->destroy)
		expr->ops->destroy(ctx, expr);
	module_put(type->owner);
}

void nft_expr_destroy(const struct nft_ctx *ctx, struct nft_expr *expr)
{
	nf_tables_expr_destroy(ctx, expr);
	kfree(expr);  // [2] UAF occurred!
}

```





## 25

26  assert(strlen(header) + strlen(content) < sizeof(http_page));

or

29 31

 tmp += sprintf(tmp, header, strlen(content));

 tmp += sprintf(tmp, "%s" content);

## 12

challenge.c:57

```c
        if (v6 != 13 && v6 != 10)
        {
            *buffer = 60;       //b'<br?'
            buffer[1] = 98;
            buffer[2] = 114;
            buffer[3] = 62;
            buffer += 4;  //57
        }
        ++i;
```

## 13



temp.c:32

```c
#define __SIZE_TYPE__ long unsigned int
    while (nleft > 0) {
        r = read(fd, nsize, nleft); //return len
        if (r < 0) {
            if (errno == EINTR || errno == EAGAIN || errno == EWOULDBLOCK)
                break;
            else
                return NET_HARDERROR;
        } else if (r == 0)
            break;

        nleft -= r; //可能溢出
        nsize += r;


        if (nleft > 0) {
            FD_ZERO(&rfdset);
            FD_SET(fd, &rfdset);
            r = select(fd + 1, &rfdset, NULL, NULL, &timeout);
            if (r < 0) {
                return NET_HARDERROR;
            }
            if (r == 0) {
                break;
            }
        }
    }
```

