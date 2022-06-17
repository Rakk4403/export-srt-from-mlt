# Export SRT(subtitle file) from MLT file(Shotcut)

If you want to make subtitle file(SRT) from MLT file(Shotcut Project file), use this.

This script exports only,
* SimpleText
* SimpleText on Video

*RichText is not supported*

## Quick

```shell
$ python export_srt.py myproject.mlt
1
00:00:02,400 --> 00:00:04,750
(몇 분 째 아무도 죽지 않고 있음)

2
00:00:04,250 --> 00:00:04,717
말랑이
...
```