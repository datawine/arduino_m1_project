<?php

define('EMAIL_FOR_REPORTS', '123@123');
define('RECAPTCHA_PRIVATE_KEY', '@privatekey@');
define('FINISH_URI', 'http://');
define('FINISH_ACTION', 'message');
define('FINISH_MESSAGE', 'Thanks for filling out my form!');
define('UPLOAD_ALLOWED_FILE_TYPES', 'doc, docx, xls, csv, txt, rtf, html, zip, jpg, jpeg, png, gif');

define('_DIR_', str_replace('\\', '/', dirname(__FILE__)) . '/');
require_once _DIR_ . '/handler.php';

?>

<?php if (frmd_message()): ?>
<link rel="stylesheet" href="<?php echo dirname($form_path); ?>/formoid-solid-blue.css" type="text/css" />
<span class="alert alert-success"><?php echo FINISH_MESSAGE; ?></span>
<?php else: ?>
<!-- Start Formoid form-->
<link rel="stylesheet" href="<?php echo dirname($form_path); ?>/formoid-solid-blue.css" type="text/css" />
<script type="text/javascript" src="<?php echo dirname($form_path); ?>/jquery.min.js"></script>
<form class="formoid-solid-blue" style="background-color:#FFFFFF;font-size:14px;font-family:'Roboto',Arial,Helvetica,sans-serif;color:#34495E;max-width:480px;min-width:150px" method="post"><div class="title"><h2>Create</h2></div>
	<div class="element-input<?php frmd_add_class("input"); ?>"><label class="title"></label><div class="item-cont"><input class="large" type="text" name="input" placeholder="姓名"/><span class="icon-place"></span></div></div>
	<div class="element-input<?php frmd_add_class("input1"); ?>"><label class="title"></label><div class="item-cont"><input class="large" type="text" name="input1" placeholder="学号"/><span class="icon-place"></span></div></div>
	<div class="element-radio<?php frmd_add_class("radio"); ?>"><label class="title">性别</label>		<div class="column column2"><label><input type="radio" name="radio" value="男" /><span>男</span></label></div><span class="clearfix"></span>
		<div class="column column2"><label><input type="radio" name="radio" value="女" /><span>女</span></label></div><span class="clearfix"></span>
</div>
	<div class="element-radio<?php frmd_add_class("radio1"); ?>"><label class="title">类别</label>		<div class="column column3"><label><input type="radio" name="radio1" value="本科" /><span>本科</span></label></div><span class="clearfix"></span>
		<div class="column column3"><label><input type="radio" name="radio1" value="硕士" /><span>硕士</span></label></div><span class="clearfix"></span>
		<div class="column column3"><label><input type="radio" name="radio1" value="博士" /><span>博士</span></label></div><span class="clearfix"></span>
</div>
	<div class="element-select<?php frmd_add_class("select"); ?>"><label class="title"></label><div class="item-cont"><div class="large"><span><select name="select" >

		<option value="建筑学">建筑学</option>
		<option value="城乡规划">城乡规划</option>
		<option value="建筑环境与能源应用工程">建筑环境与能源应用工程</option>
		<option value="土木工程">土木工程</option>
		<option value="工程管理">工程管理</option>
		<option value="水利水电工程">水利水电工程</option>
		<option value="水利科学与工程">水利科学与工程</option>
		<option value="环境工程">环境工程</option>
		<option value="环境工程（全球环境国际班）">环境工程（全球环境国际班）</option>
		<option value="给排水科学与工程">给排水科学与工程</option>
		<option value="机械工程">机械工程</option>
		<option value="机械工程（实验班）">机械工程（实验班）</option>
		<option value="测控技术与仪器">测控技术与仪器</option>
		<option value="微机电系统工程">微机电系统工程</option>
		<option value="车辆工程">车辆工程</option>
		<option value="车辆工程（汽车造型与车身设计方向）">车辆工程（汽车造型与车身设计方向）</option>
		<option value="工业工程">工业工程</option>
		<option value="能源与动力工程">能源与动力工程</option>
		<option value="能源与动力工程">能源与动力工程</option>
		<option value="工程力学">工程力学</option>
		<option value="工程力学（钱学森力学班）">工程力学（钱学森力学班）</option>
		<option value="航空航天工程">航空航天工程</option>
		<option value="电气工程及其自动化">电气工程及其自动化</option>
		<option value="电子信息科学与技术">电子信息科学与技术</option>
		<option value="电子信息工程">电子信息工程</option>
		<option value="电子科学与技术">电子科学与技术</option>
		<option value="微电子科学与工程">微电子科学与工程</option>
		<option value="自动化">自动化</option>
		<option value="软件工程">软件工程</option>
		<option value="计算机科学与技术">计算机科学与技术</option>
		<option value="计算机科学与技术（计算机科学实验班）">计算机科学与技术（计算机科学实验班）</option>
		<option value="工程物理">工程物理</option>
		<option value="工程物理（能源实验班）">工程物理（能源实验班）</option>
		<option value="核工程与核技术">核工程与核技术</option>
		<option value="高分子材料与工程">高分子材料与工程</option>
		<option value="化学工程与工业生物工程">化学工程与工业生物工程</option>
		<option value="材料科学与工程">材料科学与工程</option>
		<option value="数学与应用数学">数学与应用数学</option>
		<option value="信息与计算科学">信息与计算科学</option>
		<option value="数理基础科学（物理系）">数理基础科学（物理系）</option>
		<option value="数理基础科学（数学系）">数理基础科学（数学系）</option>
		<option value="物理学">物理学</option>
		<option value="应用物理学">应用物理学</option>
		<option value="化学">化学</option>
		<option value="化学生物学">化学生物学</option>
		<option value="生物科学">生物科学</option>
		<option value="生物技术">生物技术</option>
		<option value="行政管理">行政管理</option>
		<option value="信息管理与信息系统">信息管理与信息系统</option>
		<option value="会计学">会计学</option>
		<option value="经济与金融">经济与金融</option>
		<option value="工商管理">工商管理</option>
		<option value="金融学">金融学</option>
		<option value="经济学">经济学</option>
		<option value="社会学">社会学</option>
		<option value="国际政治">国际政治</option>
		<option value="心理学">心理学</option>
		<option value="政治学与行政学">政治学与行政学</option>
		<option value="哲学">哲学</option>
		<option value="历史学">历史学</option>
		<option value="汉语言文学">汉语言文学</option>
		<option value="英语">英语</option>
		<option value="英语（世界文学与文化实验班）">英语（世界文学与文化实验班）</option>
		<option value="日语">日语</option>
		<option value="法学">法学</option>
		<option value="法 学（国际班）">法 学（国际班）</option>
		<option value="新闻学">新闻学</option>
		<option value="广告学">广告学</option>
		<option value="艺术史论">艺术史论</option>
		<option value="动画">动画</option>
		<option value="绘画">绘画</option>
		<option value="雕塑">雕塑</option>
		<option value="摄影">摄影</option>
		<option value="中国画">中国画</option>
		<option value="艺术设计学">艺术设计学</option>
		<option value="视觉传达设计">视觉传达设计</option>
		<option value="环境设计">环境设计</option>
		<option value="产品设计">产品设计</option>
		<option value="服装与服饰设计">服装与服饰设计</option>
		<option value="公共艺术">公共艺术</option>
		<option value="工艺美术">工艺美术</option>
		<option value="数字媒体艺术">数字媒体艺术</option>
		<option value="艺术与科技">艺术与科技</option>
		<option value="陶瓷艺术设计">陶瓷艺术设计</option>
		<option value="工业设计">工业设计</option>
		<option value="临床医学">临床医学</option>
		<option value="临床医学">临床医学</option>
		<option value="生物医学工程">生物医学工程</option>
		<option value="药学">药学</option></select><i></i><span class="icon-place"></span></span></div></div></div>
	<div class="element-separator"><hr><h3 class="section-break-title">有效日期</h3></div>
	<div class="element-date<?php frmd_add_class("date"); ?>"><label class="title"></label><div class="item-cont"><input class="large" data-format="yyyy-mm-dd" type="date" name="date" placeholder="开始时间"/><span class="icon-place"></span></div></div>
	<div class="element-date<?php frmd_add_class("date1"); ?>"><label class="title"></label><div class="item-cont"><input class="large" data-format="yyyy-mm-dd" type="date" name="date1" placeholder="截止时间"/><span class="icon-place"></span></div></div>
<div class="submit"><input type="submit" value="Create"/></div></form><script type="text/javascript" src="<?php echo dirname($form_path); ?>/formoid-solid-blue.js"></script>

<!-- Stop Formoid form-->
<?php endif; ?>

<?php frmd_end_form(); ?>