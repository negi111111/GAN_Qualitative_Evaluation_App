#!/usr/local/bin/perl 
use strict;
use Encode;
use Math::Trig;
use URI::Escape;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
require 'package.cgi';
#use encoding 'utf-8';

print "Content-Type: text/html\nAllow:GET\n\n";

my @keys=("debug","D","R","A");
my %path=&get(\@keys);

my @DATA_DIRs=("collect5","collectFMD", "wgan"); #データセットとかがある場所
my $DATA_DIR="data1/$DATA_DIRs[2]";

#結果の画像パスが入ってる場所
my @RESULT_DIRs=("results","results1","results_pc","results_gd","results_pc_gd");
my $RESULT_DIR="$DATA_DIR/$RESULT_DIRs[0]";
#保存場所
my $ANSWER_DIR="$DATA_DIR";

my $CONTENT=1;
my $CLASS=10;
my $debug=$path{debug};

&base::header();
&main();
&base::tail();


sub main{
#print "<input type=\"text\" name=\"time\" value=\"$ANSWER_DIR\"/>";

	print "<form id=\"form\" action=\"answer.cgi\" method=\"post\">\n";
	print "<table border=\"0\">";
	#回答者の名前
	print "<tr>";
	print "<td>名前</td>";
	print "<td>";
	print "<input type=\"text\" name=\"name\" value=\"名前いれてね\"/>";
	print "</td>";
	print "</tr>\n";
	#時間
	print "<tr>";
	print "<td></td>";
	print "<td>";
	my $times = time();
	if($debug==1){print "<input type=\"text\" name=\"time\" value=\"$times\"/>";}
	else{print "<input type=\"hidden\" name=\"time\" value=\"$times\"/>";}
	print "</td>";
	print "</tr>\n";
	#回答保存先
	print "<tr>";
	print "<td></td>";
	print "<td>";
	if($debug==1){print "<input type=\"text\" name=\"answer_dir\" value=\"$ANSWER_DIR\"/>";}
	else{print "<input type=\"hidden\" name=\"answer_dir\" value=\"$ANSWER_DIR\"/>";}
	print "</td>";
	print "</tr>\n";
	#回答データ
	print "<tr>";
	print "<td></td>";
	print "<td>";
	if($debug==1){print "<input type=\"text\" id=\"answer_data\" name=\"answer_data\" value=\"\"/>";}
	else{print "<input type=\"hidden\" id=\"answer_data\" name=\"answer_data\" value=\"\"/>";}
	print "</td>";
	print "</tr>\n";
	print "</table>";
	print "</form>\n";
	
	#画像群
	&printImages();
	&GetImages();
	print << "EOF";
	<script> 
	var page=0;
	var max_content=$CONTENT;
	var content=0;
	var max_page=$CLASS;
	var end=0;
	</script>
EOF
	print "<script src=\"question.js\"></script>\n";
}

sub get{
	my $tar=$ENV{'QUERY_STRING'};
	my @target=split(/[=&?]/,$tar);
	my @key=@{$_[0]};
	my %path;
	foreach my $k(@key){
		$path{$k}=0;
	}
	if($#target>0){
		my $k="";
		for(my $i=1;$i<=$#target;$i++){	
			if($i%2==0){
				$path{$target[$i]}=0;
			}else{
				my $str=$target[$i];
				$str =~ s/\+/ /g;
				$str =~ s/%([0-9a-fA-F]{2})/pack("H2",$1)/eg;
				$path{$target[$i-1]}=$str;
			}
		}
	}
	foreach my $k(keys(%path)){
		#print "$k:$path{$k}\t";
	}
	return %path;
}

sub printImages{	
	my $H=9;
	my $W=9;
	print << "EOF";
	<script>
	height=$H;
	width=$W;
	</script>
EOF
	print "<div id=\"question\"></div>";
	print "<p>*「偽物」とは深層学習を利用して生成した食事画像のことです。</p>";
	print "<p>以下の画像は殆どが本物の食事画像ですが、一部はGenerative Adversarila Networksを用いて生成した「偽物」の食事画像です。</p>";
	print "<button type=\"button\" name=\"back_page\" value=\"0\" onclick=\"backPage()\"><h1>戻る</h1></button>";
	print "<button type=\"button\" name=\"back_page\" value=\"1\" onclick=\"skipPage()\"><h1>該当なし</h1></button>";
	print "<table border=\"1\">";
	for(my $i=0;$i<$H;$i++){
		print "<tr>";
		for(my $j=0;$j<$W;$j++){
			my $n=$i*$W+$j;
			print "<td><IMG id=\"image$n\" height=\"64\"  onclick=\"getInput(this);\"/></td>";
		}
		print "</tr>";
	}
	print "</table>";
}
sub GetGlobsTxt{
	my $dir=$_[0];
	my $key=$_[1];
	my @files;
	opendir(DIR,$dir);
	while(my $file=readdir(DIR)){
		if(index($file,$key)!=-1){
			push(@files,"$dir/$file");
		}
	}
	return sort(@files);
}
sub GetImages{
	print "<script type=\"text/javascript\">\n";
	print "images=[];\n";
	print "classes=[];\n";
	print "words=[];\n";
	
	my %words;
	my $file="$DATA_DIR/keyword";
	open(FILE,$file);
	while(my $line=<FILE>){
		chop($line);
		my @line_ls=split(" ",$line);
		my $class=$line_ls[0];
		my $w=$line_ls[1];
		$words{$class}=$w;
	}
	close(FILE);
	
	#my @srcf=("content0.txt","content1.txt","content2.txt","content3.txt","content4.txt","content9.txt");
	my @srcf=&GetGlobsTxt($RESULT_DIR,"content");
	#print @srcf;
	for(my $c=0;$c<=$#srcf;$c++){
		print "images[$c]=[];\n";
		my $file=$srcf[$c];
		my %src_ls;
		my @keys;
		#my $file="$RESULT_DIR/$f";
		open(FILE,$file);
		while(my $line=<FILE>){
			chop($line);
			my @line_ls=split(" ",$line);
			my $src=$line_ls[0];
			#$src=~ s/result.jpg/result_pc.jpg/g;
			my $class=$line_ls[1];
			unless(defined($src_ls{$class})){
				$src_ls{$class}=();
				push(@keys,$class);
			}
			push(@{$src_ls{$class}},$src);
		}
		close(FILE);
		
		#my @keys=sort(keys(%src_ls));
		print "classes[$c]=[];\n";
		for(my $j=0;$j<=$#keys;$j++){			
			my $k=$keys[$j];
			my $w=$words{$k};
			print "classes[$c][$j]=\"$k\";\n";
			print "words[\"$k\"]=\"$w\";\n";
			print "images[$c][$j]=[];\n";
			my $l=@{$src_ls{$k}};
			for(my $i=0;$i<$l;$i++){
				my $src=$src_ls{$k}->[$i];
				print "images[$c][$j][$i]=\"$src\";\n";
			}
		}
	}
	print "</script>\n";
	#return \%src_ls;
}


