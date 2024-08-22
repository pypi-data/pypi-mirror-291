# fast blockcheck
Track internet blocking over time

## Usage:
Could be used as tool to check access to websites 
at the moment or to measure dynamics within some period of time.  

```shell
fbc [-h] [-t TIMEOUT] [-s] [-r REPEAT]
```
To run one-time check just run program without arguments:
```shell
fbc
```

Or do measurements every minute:
```shell
fbc -r 1
```

Default timeout is 5 seconds, but it could be useful to change it:
```shell
# set request timeout to 3 seconds
fbc -t 3
```

## Features
- Can run in loop