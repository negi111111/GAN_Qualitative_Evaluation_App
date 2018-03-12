#!/usr/bin/perl --
package base;
my $base="word_content";
my $base_path="data1/generate/$base";
my $req_path="data1/requests/$base";

sub GetBase{
	return $base_path;
}
sub GetReq{
	return $req_path;
}

sub main{
	&header();
	my $n=&GetNumber();
	my @dir_ls=&GetDirList("data1/generate/style_content");
	my @src_ls;
	for my $dir (@dir_ls){
		my $src=&GetImageSrc($dir);
		push(@src_ls,$src);
	}
	print "<table>";
	print "<tr>";
	print "<td>";
	&printImageList(\@src_ls);
	print "</td>";
	print "</tr>";
	print "<table>";
	&tail();
}
sub GetNumber{
	my $tar=$ENV{'REQUEST_URI'};
	my @target=split(/[=&?]/,$tar);
	my %path;
	if($#target>1){
		my $k="";
		for(my $i=0;$i<=$#target;$i++){
			if($i%2==1){
				$path{$target[$i]}=0;
			}else{
				$path{$target[$i-1]}=$target[$i];
			}
		}
	}
	return %path;
}
sub PostNumber{
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
				$path{$target[$i-1]}=$target[$i];
			}
		}
	}
	return %path;
}

sub GetDirList{
	my @dir_ls;
	my $main=$base_path;
	open(IN,"$main/list.txt");
	while(my $line=<IN>){
		chop($line);
		push(@dir_ls,"$main/$line");
	}
	close(IN);
	@dir_ls=reverse(@dir_ls);
	return @dir_ls;
}
sub GetDirList2{
	my @dir_ls;
	my $main=$_[0];
	open(IN,"$main/list.txt");
	while(my $line=<IN>){
		chop($line);
		push(@dir_ls,"$main/$line");
	}
	close(IN);
	@dir_ls=reverse(@dir_ls);
	return @dir_ls;
}
sub GetList{
	my @dir_ls;
	my $main=$_[0];
	open(IN,"$main/list.txt");
	while(my $line=<IN>){
		chop($line);
		push(@dir_ls,"$main/$line");
	}
	close(IN);
	@dir_ls=reverse(@dir_ls);
	return @dir_ls;
}
sub GetImageSrc{
	my $img_dir=$_[0];
	my %images;
	$images{style}="$img_dir/style.jpg";
	$images{content}="$img_dir/content.jpg";
	$images{result}="$img_dir/result.jpg";
	$images{result_pc}="$img_dir/result_pc.jpg";
	$images{param}="$img_dir/param.txt";

	my @styles;
	my $c=0;
	my $stylef="$img_dir/style$c.jpg";
	while(-f $stylef){
		push(@styles,$stylef);
		$c++;
		$stylef="$img_dir/style$c.jpg";
	}
	$images{styles}=\@styles;

	my $process=0;
	if(-e $images{result}){
		$images{status}="complete";
		$process=512;
	}else{
		my $c=1;
		while($c<=512){
			my $next=sprintf("$img_dir/iter_%03d.jpg",$c);
			if(-e $next){
				$images{result}=$next;
				$process++;
			}else{
				$images{status}="$c\/512";
				last;
			}
			$c++;
		}
	}
	$images{dir}="$img_dir/";
	$images{process}=$process;
	$images{created_time}= (stat $images{result})[9];
	$images{result_gif}="$img_dir/result.gif";
	$images{mp4}="$img_dir/result.mp4";
	$images{synthesized}="$img_dir/synthesized.jpg";
	return \%images;
}
sub printDirList{
	my @dir_ls=@{$_[0]};
	my $n=$_[1];
	print "<form action=\"#\" method=\"get\">\n";
	print "<select name=\"datalist\" onchange=\"submit(this.form)\">\n";
	for(my $j=0;$j<=$#dir_ls;$j++){
		if($n == $j){
			print "<option value=\"$j\" selected>$dir_ls[$j]</option>\n";
		}else{
			print "<option value=\"$j\">$dir_ls[$j]</option>\n";
		}
	}
	print "</select>";
	print "</form>";
}
sub printImageList{
	my @src;
	if(ref($_[0]) eq 'ARRAY'){
		@src=@{$_[0]};
	}
	print "<fieldset>";
	print "<legend>スタイル変換結果一覧</legend>";
	my @key=("status","content","style","result");
	print "<table border=\"1\">";
	print "<tr>";
	foreach my $k (@key){
		print "<td>";
		print "$k";
		print "</td>";
	}
	print "</tr>";
	my $n=0;
	foreach my $t (@src){
		my %img=%{$t};
		print "<tr>";
		foreach my $k (@key){
			print "<td>";
			if($k eq "status"){
				my $time=localtime($img{created_time});
				print "$time<br>$img{$k}";
			}else{
				print "<a href=\"showImg.cgi?datalist=$n\"><IMG HEIGHT=\"128\" WIDTH=\"128\" SRC=\"$img{$k}\"/></a>\n";
			}
			print "</td>";
		}
		print "</tr>";
		$n++;
	}
	print "</table>";
	print "</fieldset>";
}

sub header{
	print << "EOF";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">
<HTML>
<HEAD>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; CHARSET=UTF-8">
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<TITLE>食事画像ユーザー評価システム</TITLE>

</HEAD>
<body style="background-color:#EDF7FF;">
<div id=header  Align="center">
<div class=opening><br>
<img src=logo.png width=200px style="display:inline-block;vertical-align:middle;">
<p>生成画像ユーザー評価システム&nbsp;&nbsp;

</p>
</div>
<div class="menu"></div>
<section id="sample-before" class="samples">
<h2>$_[0]</h2>
EOF
}
sub tail{
	print "</div></section></body></HTML>\n\n";
}

1;
