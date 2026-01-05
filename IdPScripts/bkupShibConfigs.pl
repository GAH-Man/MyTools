#!/usr/bin/perl -w

use strict;
use warnings;


my $ShibHome = '/opt/shibboleth-idp';
my $ShibConfDir = $ShibHome . '/conf';
my $ShibBkupsDir = $ShibConfDir  . '/Backups';

my @ShibConfigs;
if(@ARGV)
{
	@ShibConfigs = @ARGV;
}
else
{
	@ShibConfigs = ('attribute-filter.xml', 'attribute-resolver.xml', 'metadata-providers.xml', 'relying-party.xml', 'saml-nameid.xml');
}

unless(-e $ShibBkupsDir and -d $ShibBkupsDir)
{
	system('mkdir', $ShibBkupsDir);
}


my $dateTime = dateTime();
#print "$dateTime\n";

#my @whoami = system('whoami');
my $whoami = `whoami`;
chomp($whoami);
print "User: $whoami\n";

for(my $index = 0; $index < @ShibConfigs; $index++)
{
  #print "$ShibConfigs[$index]\n";
  my $sourceFile = $ShibConfDir . '/' . $ShibConfigs[$index];
  print "Source file:  $sourceFile\n";
  my $destinationFile = $ShibBkupsDir . '/' . $dateTime . '_' . $ShibConfigs[$index] . '.' . $whoami;
  print "Destination file:  $destinationFile\n";
  system('cp', $sourceFile, $destinationFile);
}

########################################################################################
sub dateTime
{
    my ($sec, $min, $hour, $mday, $month, $year, $wday, $yday, $isdst) = localtime();
    #my $thisday = qw(Sun Mon Tue Wed Thur Fri Sat)[(localtime)[6]];
    #$month = qw(Jan Feb Mar Apr May June July Aug Sept Oct Nov Dec)[(localtime)[4]];
    # month: Jan=0, Feb=1, Mar=3, etc.
    $year = $year + 1900;
    $month++;

  if($month < 10) {$month = '0' . $month};
  if($mday < 10) {$mday = '0' . $mday};
  if($hour < 10) {$hour = '0' . $hour};
  if($min < 10) {$min = '0' . $min};
  if($sec < 10) {$sec = '0' . $sec};
  
  #my $commentDateTime = "$year" . "$month" . "$mday" . "$hour$min$sec";
  my $commentDateTime = "$year" . "$month" . "$mday" . "_" . "$hour$min";

  return $commentDateTime;
}


sub showArray  # EUREAKA!!!!!
{
      my @array = @_;
      for(my $index=0; $index<@array; $index++)
      {
            print "$index:  $array[$index]\n";
      }
}


