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

&base::header();
&main();
&base::tail();

sub main{
	my $debug=0;
	&GetImages();
	#画像群
	&printImages();
	print "<script src=\"question.js\"></script>\n";
}
sub printImages{	
	my $H=3;
	my $W=5;
	print << "EOF";
	<script>
	height=$H;
	width=$W;
	</script>
EOF
	print "<div id=\"question\"></div>";
	print "<table border=\"1\">";
	for(my $i=0;$i<$H;$i++){
		print "<tr>";
		for(my $j=0;$j<$W;$j++){
			my $n=$i*$W+$j;
			print "<td><IMG id=\"image$n\" height=\"128\"  onclick=\"getInput(this);\"/></td>";
		}
		print "</tr>";
	}
	print "</table>";
}

sub GetImages{
	my %words;
	my $file="data/collect5/keyword";
	my @images;
	open(FILE,$file);
	while(my $line=<FILE>){
		chop($line);
		my @line_ls=split(" ",$line);
		my $class=$line_ls[0];
		my $w=$line_ls[1];
		$words{$class}=$w;
	}
	close(FILE);
	
	my @srcf=("content0.txt","content1.txt","content2.txt","content3.txt","content4.txt","content9.txt");
	for(my $c=0;$c<=$#srcf;$c++){
		my $f=$srcf[$c];
		my %src_ls;
		my $file="data/results/$f";
		open(FILE,$file);
		while(my $line=<FILE>){
			chop($line);
			my @line_ls=split(" ",$line);
			my $src=$line_ls[0];
			#$src=~ s/result.jpg/result_pc.jpg/g;
			my $class=$line_ls[1];
			unless(defined($src_ls{$class})){
				$src_ls{$class}=();
			}
			push(@{$src_ls{$class}},$src);
		}
		close(FILE);
		
		my @keys=sort(keys(%src_ls));
		for(my $j=0;$j<=$#keys;$j++){
			my $k=$keys[$j];
			my $w=$words{$k};
			my $l=@{$src_ls{$k}};
			for(my $i=0;$i<$l;$i++){
				my $src=$src_ls{$k}->[$i];
			}
		}
	}
	return (\%word,\@images);
}

