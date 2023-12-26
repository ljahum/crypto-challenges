<?php

    header('content-type:text/html;charset=utf-8');

	include('admin/databases.php');
	header("content-type:text/html;charset=utf-8");
	$username = $_POST['username'];
	$password = $_POST['password'];
	
	// 定义SQL注入关键字的黑名单
    if(preg_match('/\/|\"| |\^|or|\|\||\&|>|<|=|\-|union|mid|into|file|if|sleep|left|right|st_|floor|extractvalue|updatexml|GeomFromText|x\(|pow|rpad|repeat|join|buffer|increment|info|sys|limit|by|insert|update|delete|information_schema|;|instr|lpad|ltrim|handler|rand|floor|extractValue|geometrycollectio|polygon|multipoint|linestring|create/is',$_POST['password']))
        {
            die("<script >alert('hack!!!');window.location.href=\"login.html\";</script>");
        }    if(preg_match('/\/|\"| |\^|or|\|\||\&|>|<|=|\-|union|mid|into|file|if|sleep|left|right|st_|floor|extractvalue|updatexml|GeomFromText|x\(|pow|rpad|repeat|join|buffer|increment|info|sys|limit|by|insert|update|delete|information_schema|;|instr|lpad|ltrim|handler|rand|floor|extractValue|geometrycollectio|polygon|multipoint|linestring|create/is',$_POST['username']))
        {
            die("<script >alert('hack!!!');window.location.href=\"login.html\";</script>");
        }
        // 检测用户输入是否匹配黑名单关键字
        if (preg_match("/(" . implode('|', $blacklist) . ")/i", $username) || preg_match("/(" . implode('|', $blacklist) . ")/i", $password)) {
    // 如果用户名或密码包含黑名单关键字，替换黑名单关键字为空
         $username = str_ireplace($blacklist, "", $username);
         $password = str_ireplace($blacklist, "", $password);
          $sql = "SELECT * FROM user WHERE username = '$username' AND password = '$password'";
         echo $sql;    
        }else{
        $sql = "SELECT * FROM user WHERE username = '$username' AND password = '$password'";
        }
    
	$result = mysqli_query($link,$sql);
        $num = mysqli_num_rows($result);
	if($username==="admin"&&$num){
        session_start();

       // 在验证用户后，如果登录成功，设置会话变量来表示用户已登录
        $_SESSION['loggedin'] = true;
        $_SESSION['username'] = 'admin'; // 用户名
        $_SESSION['role'] = 'admin'; // 用户角色或权限
	echo "<script>window.location.href='./admin/admin.html';</script>";
	}
	else if($num){
	     echo "<script>window.location.href='home.php';</script>";
	}else{
	echo"<script>alert('登录失败')</script>";
	echo "<script>window.location.href='login.html';</script>";
	}
	mysqli_close($link);
