Git has a limit of 4096 characters for a filename, except on Windows when Git is compiled with msys. It uses an older version of the Windows API and there's a limit of 260 characters for a filename.

So as far as I understand this, it's a limitation of msys and not of Git. You can read the details here: [https://github.com/msysgit/git/pull/110](https://github.com/msysgit/git/pull/110)

You can circumvent this by using another Git client on Windows or set `core.longpaths` to `true` as explained in other answers.

```
git config --system core.longpaths true
```

Git is build as a combination of scripts and compiled code. With the above change some of the scripts might fail. That's the reason for core.longpaths not to be enabled by default.

The windows documentation at [https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=cmd#enable-long-paths-in-windows-10-version-1607-and-later](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=cmd#enable-long-paths-in-windows-10-version-1607-and-later) has some more information:
