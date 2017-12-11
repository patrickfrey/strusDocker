#!/usr/bin/perl

use strict;
use warnings;
use 5.012;
use utf8;
use Encode qw(decode encode);

my %nametab = ();
my @rulelist = ();

# Take a line with a name and make pattern matcher rules out of it
sub getRules
{
	my ($line) = @_;
	$line =~ s/^\s+//;	# ltrim
	$line =~ s/\s+$//;	# rtrim
	$line =~ s/\s+/ /g;	# remove duplicate spaces
	my $origname = '';
	my $convname = '';
	my $ch;
	my @origrule = ();
	my @convrule = ();

	foreach $ch( split('', $line))
	{
		if ($ch =~ m/[a-zA-Z]/)
		{
			$convname .= $ch;
			$origname .= $ch;
		}
		elsif ($ch eq ' ')
		{
			$nametab{ $convname} = $origname;
			push( @origrule, $origname); $origname = '';
			push( @convrule, $convname); $convname = '';
		}
		else
		{
			my $chnum = ord($ch);
			my $chhex = sprintf( "%X", $chnum);
			$origname .= $ch;
			$convname .= "_$chhex";
		}
	}
	if (length( $origname) > 0) {
		$nametab{ $convname} = encode("utf-8", $origname);
		push( @origrule, $origname); $origname = '';
		push( @convrule, $convname); $convname = '';
	}
	my $convrulename = join( '_', @convrule);
	my $rulelen = $#convrule + 1;
	my $ruleargs = '_' . join( ', _', @convrule);
	my $rule = $convrulename . '= within( ' . $ruleargs . ' | ' . $rulelen . ");";
	push( @rulelist, $rule);
}


print( "%MATCHER exclusive\n");
while (<>)
{
	chomp;
	getRules( decode("utf-8", $_));
}

foreach my $name (sort keys %nametab) {
	my $seq = $nametab{$name};
	# print( "_$name" . " : /$seq/ ~$edist;\n");
	print( "_$name" . " : /$seq/;\n");
}
print "\n";
foreach my $rule (@rulelist) {
	print "$rule\n";
}
print "\n";



