-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: music
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `artists`
--

DROP TABLE IF EXISTS `artists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `artists` (
  `ArtistID` char(4) NOT NULL,
  `ArtistName` text NOT NULL,
  `Biography` text,
  PRIMARY KEY (`ArtistID`),
  UNIQUE KEY `SingerID_UNIQUE` (`ArtistID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `artists`
--

LOCK TABLES `artists` WRITE;
/*!40000 ALTER TABLE `artists` DISABLE KEYS */;
INSERT INTO `artists` VALUES ('p000','无',NULL),('p001','苏打绿','苏打绿（Sodagreen），成立于2001年，是中国台湾的一个独立音乐乐队，成员包括青峰（吴青峰，主唱）、阿福（谢馨仪，贝斯手）、家凯（刘家凯，键盘手）、阿龚（龚钰祺，鼓手）、阿玮（何景扬，吉他手）和小威（史俊威，大提琴手）。苏打绿以其清新、自然的音乐风格和独特的嗓音著称，代表作品有《小情歌》、《你在烦恼什么》、《无与伦比的美丽》等。乐队以独特的音乐风格和深情的歌词在华语乐坛中占有重要地位。'),('p002','凤凰传奇','凤凰传奇，成立于2004年，是中国内地的一支流行音乐组合，成员包括曾毅和玲花（杨魏玲花）。他们的音乐融合了流行、民族、电子等多种元素，以欢快、动感的风格著称。代表作品有《月亮之上》、《最炫民族风》、《自由飞翔》等。凤凰传奇凭借其独特的音乐风格和广泛的观众基础，在中国内地乐坛中享有较高的知名度。'),('p003','周杰伦','周杰伦（Jay Chou），1979年1月18日出生于中国台湾，是华语乐坛的著名歌手、词曲创作人、音乐制作人和导演。他以独特的音乐风格和创新的音乐理念著称，结合了R&B、嘻哈、古典、摇滚等多种音乐元素。代表作品有《双截棍》、《晴天》、《稻香》、《青花瓷》等。周杰伦的音乐风格多样化，被誉为“亚洲流行天王”，对华语流行音乐的发展产生了深远的影响。'),('p004','李宇春','李宇春，1984年3月10日出生于中国四川省，是中国内地的流行歌手、演员和音乐制作人。她因2005年在超级女声选秀比赛中获得冠军而一举成名。代表作品有《下个，路口，见》、《和你一样》、《再不疯狂我们就老了》等。李宇春以其独特的嗓音和个性化的音乐风格在华语乐坛中占有重要地位，并在音乐、影视等多个领域取得了不俗的成绩。'),('p005','张学友','张学友（Jacky Cheung），1961年7月10日出生于中国香港，是华语乐坛的著名歌手和演员。他被誉为“歌神”，以其卓越的歌唱技巧和深情的演唱风格著称。代表作品有《吻别》、《祝福》、《一千个伤心的理由》、《她来听我的演唱会》等。张学友在华语乐坛中拥有广泛的影响力，并在音乐、电影等多个领域取得了卓越的成就。'),('p006','五月天','五月天（Mayday），成立于1997年，是中国台湾的一个摇滚乐队，成员包括阿信（陈信宏，主唱）、怪兽（温尚翊，吉他手）、石头（石锦航，吉他手）、玛莎（蔡升晏，贝斯手）和冠佑（刘冠佑，鼓手）。他们以其青春洋溢的音乐风格和励志的歌词著称，代表作品有《倔强》、《突然好想你》、《温柔》、《你不是真正的快乐》等。五月天被誉为“华语乐坛的摇滚天团”，对华语摇滚乐的发展产生了重要影响。'),('p007','黑鸭子演唱组',NULL),('p008','张靓颖',NULL),('p009','伍佰 & China Blue',NULL),('p010','王菀之',NULL),('p011','于莎莎',NULL),('p012','派伟俊',NULL),('p013','张含韵',NULL),('p014','张杰',NULL),('p015','图拉',NULL),('p016','syE_21',NULL),('p017','郭富城',NULL),('p018','王麟',NULL),('p019','吴昕',NULL),('p020','任素汐',NULL),('p021','温岚',NULL),('p022','王心凌',NULL),('p023','陈奕迅',NULL),('p024','刘岩',NULL),('p025','关正杰',NULL),('p026','汤潮',NULL),('p027','Ariana Grande',NULL),('p028','王智',NULL),('p029','水木年华',NULL),('p030','曹芙嘉',NULL),('p031','阿尔法',NULL),('p032','蒋志光',NULL),('p033','刘德华',NULL),('p034','陈洁仪',NULL),('p035','刘若英',NULL),('p036','金美儿',NULL),('p037','王丽坤',NULL),('p038','毛不易',NULL),('p039','G.E.M. 邓紫棋',NULL),('p040','赵今麦',NULL),('p041','易铭',NULL),('p042','王俊凯',NULL),('p043','王杰',NULL),('p044','蔡枫华',NULL),('p045','小六',NULL),('p046','王菲',NULL),('p047','林志炫',NULL),('p048','周云蓬',NULL),('p049','TF家族-穆祉丞',NULL),('p050','刘全和',NULL),('p051','马兰花',NULL),('p052','叶蒨文',NULL),('p053','林俊杰',NULL),('p054','那英',NULL),('p055','梅艳芳',NULL),('p056','王力宏',NULL),('p057','Ella陈嘉桦',NULL),('p058','林珈含',NULL),('p059','许钧',NULL),('p060','韦绮姗',NULL),('p061','田馥甄',NULL),('p062','郑中基',NULL),('p063','邝美云',NULL),('p064','张国荣',NULL),('p065','苏永康',NULL),('p066','K\'naan',NULL),('p067','费玉清',NULL),('p068','高慧君',NULL),('p069','庾澄庆',NULL),('p070','成龙',NULL),('p071','陈淑桦',NULL),('p072','Free 9',NULL),('p073','小精灵',NULL),('p074','阿鲁阿卓',NULL),('p075','赵楚纶',NULL),('p076','潘玮柏',NULL),('p077','钟立风',NULL),('p078','Lara梁心颐',NULL),('p079','五月天 阿信',NULL),('p080','刘思良',NULL),('p081','CoCo李玟',NULL),('p082','林子祥',NULL),('p083','萧敬腾',NULL),('p084','华晨宇',NULL),('p085','贰佰',NULL),('p086','达布希勒图',NULL),('p087','Priscilla Ahn',NULL),('p088','赵大紫',NULL),('p089','易烊千玺',NULL),('p090','罗志祥',NULL),('p091','丁当',NULL),('p092','刘姝麟',NULL),('p093','MC赵小涣',NULL),('p094','郁可唯',NULL),('p095','伊能静',NULL),('p096','小娟&山谷里的居民',NULL),('p097','三十位素人',NULL),('p098','李健',NULL),('p099','TF家族-陈天润',NULL),('p100','Jeffrey董又霖',NULL),('p101','张震岳',NULL),('p102','杨光',NULL),('p103','海陆',NULL),('p104','陈慧娴',NULL),('p105','郑伊健',NULL),('p106','小沈阳',NULL),('p107','张智霖',NULL),('p108','李克勤',NULL),('p109','吕薇',NULL),('p110','华语群星',NULL),('p111','许秋怡',NULL),('p112','周炜',NULL),('p113','陈梓童',NULL),('p114','刘嘉玲',NULL),('p115','光良',NULL),('p116','宁静',NULL),('p117','TF家族-左航',NULL),('p118','刘一扬',NULL),('p119','张萌',NULL),('p120','李幸倪',NULL),('p121','许志安',NULL),('p122','罗文',NULL),('p123','许飞',NULL),('p124','任贤齐',NULL),('p125','齐秦',NULL),('p126','黄圣依',NULL),('p127','蔡依林',NULL),('p128','童安格',NULL),('p129','张鑫',NULL),('p130','浪花兄弟',NULL),('p131','李玲玉',NULL),('p132','阿朵',NULL),('p133','朱婧汐Akini Jing',NULL),('p134','甄妮',NULL),('p135','郑希怡',NULL),('p136','王源',NULL),('p137','MC HotDog 热狗',NULL),('p138','房东的猫',NULL),('p139','袁咏琳',NULL),('p140','周兴才让',NULL),('p141','Jinx周',NULL),('p142','丢火车乐队',NULL),('p143','LOKEY低调组合',NULL),('p144','丁于',NULL),('p145','庄达菲',NULL),('p146','余味无穷',NULL),('p147','汤宝如',NULL),('p148','黎明',NULL),('p149','SNH48',NULL),('p150','严爵',NULL),('p151','阿达娃',NULL),('p152','陈绮贞',NULL),('p153','黄静美',NULL),('p154','徐小凤',NULL),('p155','李硕',NULL),('p156','汪正正',NULL),('p157','TF家族-余宇涵',NULL),('p158','汪峰',NULL),('p159','李荣浩',NULL),('p160','林仟淇',NULL),('p161','林姗姗',NULL),('p162','李明霖',NULL),('p163','许鹤缤',NULL),('p164','林迈可',NULL),('p165','蔡国权',NULL),('p166','许茹芸',NULL),('p167','胡月',NULL),('p168','杨瑞代',NULL),('p169','王雅文',NULL),('p170','TF家族-朱志鑫',NULL),('p171','徐静雨',NULL),('p172','张韶涵',NULL),('p173','赵星',NULL),('p174','李安',NULL),('p175','TF家族-姚昱辰',NULL),('p176','黄渤',NULL),('p177','萧秉治',NULL),('p178','郑秀文',NULL),('p179','风子',NULL),('p180','刘欢',NULL),('p181','刘莉旻',NULL),('p182','TF家族-邓佳鑫',NULL),('p183','马郁',NULL),('p184','潘越云',NULL),('p185','关诗敏',NULL),('p186','黎瑞恩',NULL),('p187','万晓利',NULL),('p188','李艳恰+刘洋',NULL),('p189','钟镇涛',NULL),('p190','YC',NULL),('p191','金莎',NULL),('p192','TF家族-童禹坤',NULL),('p193','周华健',NULL),('p194','阿木古楞',NULL),('p195','刘劲',NULL),('p196','法老',NULL),('p197','张苗苗',NULL),('p198','潘儿',NULL),('p199','张惠妹',NULL),('p200','钟丽缇',NULL),('p201','谭咏麟',NULL),('p202','彭羚',NULL),('p203','周慧敏',NULL),('p204','徐千雅',NULL),('p205','陈美玲',NULL),('p206','蓝盈莹',NULL),('p207','TFBOYS',NULL),('p208','董雪一家',NULL),('p209','阿梨粤',NULL),('p210','周润发',NULL),('p211','雷佳',NULL),('p212','Glay',NULL),('p213','阿哲',NULL),('p214','王淑瑶',NULL),('p215','孙燕姿',NULL),('p216','乌兰图雅',NULL),('p217','毛阿敏',NULL),('p218','宝石Gem',NULL),('p219','谷村新司',NULL),('p220','筷子兄弟',NULL),('p221','艾敬',NULL),('p222','黄龄',NULL),('p223','王祖蓝',NULL),('p224','斯琴高丽',NULL),('p225','好妹妹',NULL),('p226','告五人',NULL),('p227','舒克',NULL),('p228','TF家族-张峻豪',NULL),('p229','叶振棠',NULL),('p230','张雨绮',NULL),('p231','小河与寻谣计划',NULL),('p232','王旭《旭日阳刚》',NULL),('p233','赵尔玲',NULL),('p234','刘芸',NULL),('p235','TF家族-苏新皓',NULL),('p236','草蜢',NULL),('p237','孜克肉拉木?艾尼',NULL),('p238','谢霆锋',NULL),('p239','刘小慧',NULL),('p240','沈梦辰',NULL),('p241','吕方',NULL),('p242','赵冠羽',NULL),('p243','蒋先贵',NULL),('p244','Kobe Bryant',NULL),('p245','齐豫',NULL),('p246','周影',NULL),('p247','关淑怡',NULL),('p248','赵学而',NULL),('p249','豆包',NULL),('p250','韩红',NULL),('p251','李鑫一',NULL),('p252','陈知远',NULL),('p253','TF家族-张极',NULL),('p254','白冰',NULL),('p255','陶喆',NULL),('p256','陈松伶',NULL),('p257','马条',NULL),('p258','周启生',NULL),('p259','李斯丹妮',NULL),('p260','万茜',NULL),('p261','邓丽君',NULL),('p262','张家辉',NULL),('p263','张羽',NULL),('p264','彭席彦',NULL),('p265','张若水',NULL),('p266','金波',NULL),('p267','Soler',NULL),('p268','S.H.E',NULL),('p269','柳爽',NULL),('p270','钟皓天',NULL),('p271','黄凯芹',NULL),('p272','金晨',NULL),('p273','孟佳',NULL),('p274','欧丁玉',NULL),('p275','羽田',NULL),('p276','何炅',NULL),('p277','邓超',NULL),('p278','TF家族-张泽禹',NULL),('p279','王霏霏',NULL),('p280','Pada',NULL),('p281','平安',NULL),('p282','玖月奇迹',NULL),('p283','刘全利',NULL);
/*!40000 ALTER TABLE `artists` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-18 16:26:38
