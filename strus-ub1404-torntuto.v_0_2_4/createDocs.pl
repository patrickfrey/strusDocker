#!/usr/bin/perl

use strict;
use warnings;
use 5.010;

my $continent = '';
my %capital_map = ();
my %continent_map = ();
my %language_map = ();

sub trim
{
	my ($arg) = @_;
	$arg =~ s/^\s+//g;
	$arg =~ s/\s+$//g;
	return $arg;
}

sub entitySubs
{
	my ($arg) = @_;
	$arg =~ s/'/\&quot\;/g;
	return $arg;
}

open COUNTRIES, "<./countries.txt" or die "failed to open file ./countries.txt for reading ($!)\n";
while (<COUNTRIES>)
{
	chomp;
	my $ln = $_;
	if ($ln =~ m/==(.*)/)
	{
		$continent = trim( $1);
	}
	elsif ($ln =~ m/[,]/)
	{
		my ($country, $capital) = split( ',', $ln, 2);
		if ($country && $capital)
		{
			$country = entitySubs( trim( $country));
			$capital = entitySubs( trim( $capital));
			$capital_map{ $country } = $capital;
			$continent_map{ $country } = $continent;
		}
	}
}
close COUNTRIES;

open LANGUAGES, "<./languages.txt" or die "failed to open file ./languages.txt for reading ($!)\n";
while (<LANGUAGES>)
{
	chomp;
	my $ln = $_;
	if ($ln =~ m/=/)
	{
		my ($country, $lang) = split( '=', $ln, 2);
		if ($country && $lang)
		{
			$country = entitySubs( trim($country));
			$lang = trim($lang);
			$language_map{ $country } = $lang;
		}
	}
}
close LANGUAGES;

my @keylist = ();
foreach my $cl( keys %language_map)
{
	if ($capital_map{ $cl })
	{
		$keylist[ $#keylist+1] = $cl;
	}
	else
	{
		print STDERR "missing capital of '$cl'\n";
	}
}
@keylist = sort( @keylist);

foreach my $cc( keys %capital_map)
{
	unless ($language_map{ $cc })
	{
		print STDERR "missing language of '$cc'\n";
	}
}

print "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>\n";
print "<list>\n";

foreach my $country( @keylist)
{
	my $capital = $capital_map{ $country };
	my $continent = $continent_map{ $country };
	my $languages = $language_map{ $country };
	print "<doc id='$country'>In the country <country id='$country'>$country</country> in <continent id='$continent'>$continent</continent> with the <capital id='$capital'>$capital</capital> are the following languages spoken: $languages.</doc>\n";
}

print "</list>\n";

