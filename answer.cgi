#!/usr/local/bin/perl
use strict;
use Encode;
use Math::Trig;
#use encoding 'utf-8';
require 'package.cgi';

print "Content-Type: text/html\nAllow: GET\n\n";

base::header();
&main();
base::tail();

sub main{	

	my %path=&post();
	my $file=&setAnswerFile($path{answer_dir});
	my $g_data=$path{answer_data};
	my @g_ls=split(" ",$g_data);
	
	my %answers;
	my $acc=0;
	my $c=0;
	#print "<h1>あなたの回答結果</h1>";
	#print "<h1>$g_data</h1>";
	foreach my $ans (@g_ls){
		my @q_a=split(":",$ans);
		$answers{$q_a[0]}=$q_a[1];
		my @q_content_class=split("_",$q_a[0]);
		my @a_class_cluster=split("_",$q_a[1]);
		#if($q_content_class[1] eq $a_class_cluster[0]){
		if("0000"eq $a_class_cluster[0]){
			$acc+=1;
		}
		$c+=1;
	}
	$acc/=10;
	$acc*=100;
	
	open(OUT,">$file");
	print OUT "$path{name},$path{time}\n";
	foreach my $key (sort(keys(%answers))){
		print OUT "$key $answers{$key}\n";
	}
	close(OUT);
	system("chmod 777 $file");
	
	my $times = time();
	my $taken_time=$times-$path{time};
	print "<h1>回答時間:$taken_time秒</h1>";
	print "<h1>正答率：$acc\%</h1>";
	print "<h1>ご協力ありがとうございました！</h1>";
}

sub setAnswerFile{
	my $dir=$_[0];
	unless(-d $dir){
		system("mkdir $dir");
		system("chmod 777 $dir");
	}
	my $n=0;
	my $file="$dir/answer$n.txt";
	while(-e $file){
		$n++;
		$file="$dir/answer$n.txt";
	}
	return $file;
}
sub post{
	my $tar;
	read(STDIN, $tar, $ENV{'CONTENT_LENGTH'});
	my @target=split(/[=&?]/,$tar);
	my %path;
	if($#target>0){
		my $k="";
		for(my $i=0;$i<=$#target;$i++){	
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
	return %path;
}
