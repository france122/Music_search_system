CREATE DATABASE  IF NOT EXISTS `music` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `music`;
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
-- Table structure for table `albums`
--

DROP TABLE IF EXISTS `albums`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `albums` (
  `AlbumID` char(4) NOT NULL,
  `AlbumName` text NOT NULL,
  `ArtistID` char(4) NOT NULL,
  PRIMARY KEY (`AlbumID`),
  UNIQUE KEY `AlbumID_UNIQUE` (`AlbumID`),
  KEY `FK_albums_artistID_idx` (`ArtistID`),
  CONSTRAINT `FK_albums_artistID` FOREIGN KEY (`ArtistID`) REFERENCES `artists` (`ArtistID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `albums`
--

LOCK TABLES `albums` WRITE;
/*!40000 ALTER TABLE `albums` DISABLE KEYS */;
INSERT INTO `albums` VALUES ('0','无','p000'),('a101','小宇宙','p001'),('a102','无与伦比的美丽','p001'),('a103','春 日光','p001'),('a104','夏／狂热','p001'),('a105','你在烦恼什么','p001'),('a106','秋：故事','p001'),('a107','冬 未了','p001'),('a108','同名专辑','p001'),('a109','Shadow','p001'),('a110','原汁原味','p001'),('a111','十年一刻','p001'),('a112','Walk Together','p001'),('a113','Believe in Music','p001'),('a201',' 月亮之上','p002'),('a202',' 吉祥如意','p002'),('a203',' 最炫民族风','p002'),('a204',' 我从草原来','p002'),('a205',' 大声唱','p002'),('a206',' 最好的时代','p002'),('a207',' 远方的远方还是远方','p002'),('a208','听见中国听见你','p002'),('a209','中国喜事','p002'),('a210','荷塘月色','p002'),('a211','天籁传奇','p002'),('a212','舞动奇迹','p002'),('a301',' Jay','p003'),('a302',' 范特西','p003'),('a303',' 八度空间','p003'),('a304',' 叶惠美','p003'),('a305',' 七里香','p003'),('a306',' 十一月的肖邦','p003'),('a307',' 依然范特西','p003'),('a308',' 我很忙','p003'),('a309',' 魔杰座','p003'),('a310',' 跨时代','p003'),('a311',' 惊叹号','p003'),('a312',' 十二新作','p003'),('a313',' 哎呦，不错哦','p003'),('a314',' 周杰伦的床边故事','p003'),('a315',' 最伟大的作品','p003'),('a401','周末愉快','p004'),('a402','在吗？','p004'),('a403','野蛮生长','p004'),('a404','再不疯狂我们就老了','p004'),('a405','李宇春','p004'),('a406','少年中国','p004'),('a407','皇后与梦想','p004'),('a501','偷心','P005'),('a502','传奇 - 我与你','P005'),('a503','遥远的她?Amour','P005'),('a504','张学友精选集','P005'),('a505','吻别','P005'),('a506','只愿一生爱一人','P005'),('a507','学友．热','P005'),('a508','祝福','P005'),('a509','忘记你我做不到','P005'),('a510','情不禁','P005'),('a511','三年两语','P005'),('a512','不后悔','P005'),('a513','真爱 新曲 + 真正精选','P005'),('a514','过敏世界','P005'),('a515','走过1999','P005'),('a516','宝丽金真开心精选 1','P005'),('a517','真情流露','P005'),('a518','梦中的你','P005'),('a519','这个冬天不太冷','P005'),('a520','青梅竹马101','P005'),('a521','感冒前后 新曲加精选','P005'),('a522','宝丽金25周年 为全世界歌唱会','P005'),('a523','邓丽君15周年但愿人长久','P005'),('a524','在你身边','P005'),('a525','左右为难','P005'),('a526','有个人','P005'),('a527','饿狼传说','P005'),('a528','活出生命Live演唱会 (Live','P005'),('a529','爱.火.花','P005'),('a530','释放自己','P005'),('a531','25周年 SMILE','P005'),('a532','追忆似水芳华','P005'),('a533','Back to Priscilla 30周年演唱会','P005'),('a534','醒着做梦','P005'),('a535','2007世界巡回演唱会','P005'),('a536','精装歌集','P005'),('a537','情无四归','P005'),('a538','学友精选','P005'),('a539','想和你去吹吹风','P005'),('a540','相爱','P005'),('a541','不老的传说','P005'),('a542','又十年','P005'),('a543','敌人','P005'),('a544','一颗不变心','P005'),('a545','他在那里','P005'),('a546','Jacky Cheung 15','P005'),('a547','环球/宝丽金40周年经典101','P005'),('a548','拥友','P005'),('a549','40th Anniversary 银河岁月谭咏麟演唱会','P005'),('a550','1999友个人演唱会','P005'),('a551','金曲精选 1985-1990','P005'),('a552','旗开得胜','P005'),('a553','greatest hits 新曲+精选','P005'),('a554','忘记他','P005'),('a555','情缘十载','P005'),('a556','每天爱你多一些演唱会\'91','P005'),('a557','东成西就 电影原声带','P005'),('a558','当我想起你','P005'),('a559','音乐之旅Live演唱会','P005'),('a560','93学与友演唱会','P005'),('a561','学友 经典 世界巡回演唱会 香港站 再见篇','P005'),('a562','如果·爱 电影原声带','P005'),('a563','Black & White','P005'),('a564','张学友 爱得比你深','P005'),('a565','等你等到我心痛','P005'),('a566','就怕老歌带DJ','P005'),('a567','给我亲爱的','P005'),('a568','张学友1987-1999经典演唱会全集-95友学友演唱会','P005'),('a569','张学友87\'演唱会','P005'),('a570','一生跟你走 - 张学友年度代表作品辑','P005'),('a571','JACKY','P005'),('a572','偷心 (DJ版','P005'),('a573','爱与交响乐 / 音乐无疆界演唱会','P005'),('a574','澳门风云3 电影原声带','P005'),('a575','雪狼湖','P005'),('a576','一期一会 邝美云精选集','P005'),('a577','天下第一流','P005'),('a578','好情歌演唱会','P005'),('a579','学友光年世界巡回演唱会’07-香港站','P005'),('a580','宝丽金廿五周年连年真开心','P005'),('a581','张学友1/2世纪演唱会','P005'),('a582','学友 经典 世界巡回演唱会 台北站','P005'),('a583','日出时让街灯安睡','P005'),('a584','10 X 10 我至爱演唱会 (Live','P005'),('a585','浓情浪漫','P005'),('a586','宝丽金88极品音色系列之天碟驾到','P005'),('a587','Mui Music Show','P005'),('a588','学友光年世界巡回演唱会’07-台北站','P005'),('a589','环球巨星影音启示录','P005'),('a590','劲之碟','P005'),('a591','昨夜梦魂中','P005'),('a592','Life Is Like A Dream','P005'),('a593','定风波','P005'),('a594','RaRaRa 超嗨神曲','P005'),('a595','All Time Favourites','P005'),('a601','自传','p006'),('a602','后青春期的诗','p006'),('a603','步步 自选作品辑 the Best of 1999-2013','p006'),('a604','神的孩子都在跳舞','p006'),('a605','第二人生（明日版）','p006'),('a606','玫瑰少年','p006'),('a607','知足 最真杰作选','p006'),('a608','爱情万岁','p006'),('a609','离开地球表面 Jump!','p006'),('a610','因为你 所以我','p006'),('a611','为爱而生','p006'),('a612','第二人生 (末日版','p006'),('a613','刻在我心底的名字','p006'),('a614','为你写下这首情歌','p006'),('a615','第一张创作专辑','p006'),('a616','将军令','p006'),('a617','因你 而在','p006'),('a618','温柔 #MaydayBlue20th','p006'),('a619','小太阳','p006'),('a620','五月天 突然好想见到你 live in the sky','p006'),('a621','十万人出头天LIVE','p006'),('a622','五月天 人生无限公司 Life Live 完整收录篇','p006'),('a623','凡人歌','p006'),('a624','超级星光PK宝典','p006'),('a625','时光机','p006'),('a626','快乐天堂 滚石30演唱会','p006'),('a627','五月天 人生无限公司 Life Live 好友加班篇','p006'),('a628','唯一','p006'),('a629','Final Home 当我们混在一起','p006'),('a630','来看我们的演唱会 第5期','p006'),('a631','诺亚方舟 世界巡回演唱会','p006'),('a632','音乐电影-五月之恋','p006'),('a633','追梦3DNA 电影原声音乐','p006'),('a634','什么歌','p006'),('a635','DNA','p006'),('a636','YOUR LEGEND～燃ゆる命～','p006'),('a637','五月天 好好好想见到你 Mayday fly to 2022 线上特别版 LIVE','p006'),('a638','志明与春娇','p006'),('a639','一半人生','p006'),('a640','夜猫','p006'),('a641','我爱上的','p006'),('a642','我们是五月天','p006'),('a643','勇敢','p006'),('a644','你的神曲','p006'),('a645','欣赏','p006'),('a646','知足','p006'),('a647','2013 华语最精选','p006'),('a648','D.N.A LIVE! 五月天创造 小巨蛋演唱会创纪录音','p006'),('a649','大开天窗','p006'),('a650','外人','p006'),('a651','盛夏光年 电影原声带','p006'),('a652','2GETHER 4EVER ENCORE 演唱会影音馆','p006'),('a653','疯狂世界 #MaydayBlue20th','p006'),('a654','人生海海','p006'),('a655','First Day','p006'),('a656','你要去哪里台湾巡回演唱会Live全纪录','p006'),('a657','精彩音乐汇','p006'),('a658','转眼（2018 自传最终章）','p006'),('a659','好的情人','p006'),('a660','落跑吧爱情 电影原声带','p006'),('a661','那些你不要的','p006'),('a662','华语流行现场10','p006'),('a663','I Will Carry You','p006'),('a664','康巴情(舞曲版','p006'),('a665','在路上','p006'),('a666','纯真 #MaydayBlue20th','p006'),('a667','相信音乐金曲合辑2','p006'),('a668','逆转胜 电影原声带','p006');
/*!40000 ALTER TABLE `albums` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-02 19:17:22