## Execute to see a meta strftime documentation in console
from time import strftime
text = """\n## Time format string special character: exemple  - description ##
Exemples use execution time : %Y-%m-%d %H:%M:%S

%%a: %a  - Locale’s abbreviated weekday name.
%%A: %A  - Locale’s full weekday name.
%%b: %b  - Locale’s abbreviated month name.
%%B: %B  - Locale’s full month name.
%%c: %c  - Locale’s appropriate date and time representation.
%%d: %d  - Day of the month as a decimal number [01,31].
%%H: %H  - Hour (24-hour clock) as a decimal number [00,23].
%%I: %I  - Hour (12-hour clock) as a decimal number [01,12].
%%j: %j  - Day of the year as a decimal number [001,366].
%%m: %m  - Month as a decimal number [01,12].
%%M: %M  - Minute as a decimal number [00,59].
%%p: %p  - Locale’s equivalent of either AM or PM.
    note : When used with the strptime() function, the %%p directive only affects the output hour field if the %%I directive is used to parse the hour.

%%S: %S  - Second as a decimal number [00,61].
    note : The range really is 0 to 61; this accounts for leap seconds and the (very rare) double leap seconds.

%%U: %U  - Week number of the year (Sunday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Sunday are considered to be in week 0.
%%w: %w  - Weekday as a decimal number [0(Sunday),6].
%%W: %W  - Week number of the year (Monday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Monday are considered to be in week 0.
    note : When used with the strptime() function, %%U and %%W are only used in calculations when the day of the week and the year are specified.

%%x: %x  - Locale’s appropriate date representation.
%%X: %X  - Locale’s appropriate time representation.
%%y: %y  - Year without century as a decimal number [00,99].
%%Y: %Y  - Year with century as a decimal number.
%%Z: %Z  - Time zone name (no characters if no time zone exists).
%%%: %%  - A literal '%%' character.
"""

print( strftime(text) )
