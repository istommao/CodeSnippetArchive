# Tmux

## 安装

```bash
# Ubuntu 或 Debian
sudo apt-get install tmux

# CentOS 或 Fedora
sudo yum install tmux

# Mac
brew install tmux
```

## 开启会话

```bash
tmux new -s {session-name}
```

## 分离会话

```bash
tmux detach

or

Ctrl+b d
```

## 列出会话

```bash
tmux ls

or 

tmux list-session
```


## 进入会话

```bash
tmux attach-session -t {session-name}

or

tmux a -t {session-name}
```

## 窗格快捷键

- Ctrl+b %：划分左右两个窗格。
- Ctrl+b "：划分上下两个窗格。
- Ctrl+b <arrow key>：光标切换到其他窗格。<arrow key>是指向要切换到的窗格的方向键，比如切换到下方窗格，就按方向键↓。
- Ctrl+b ;：光标切换到上一个窗格。
- Ctrl+b o：光标切换到下一个窗格。
- Ctrl+b {：当前窗格与上一个窗格交换位置。
- Ctrl+b }：当前窗格与下一个窗格交换位置。
- Ctrl+b Ctrl+o：所有窗格向前移动一个位置，第一个窗格变成最后一个窗格。
- Ctrl+b Alt+o：所有窗格向后移动一个位置，最后一个窗格变成第一个窗格。
- Ctrl+b x：关闭当前窗格。
- Ctrl+b !：将当前窗格拆分为一个独立窗口。
- Ctrl+b z：当前窗格全屏显示，再使用一次会变回原来大小。
- Ctrl+b Ctrl+<arrow key>：按箭头方向调整窗格大小。
- Ctrl+b q：显示窗格编号。


## 窗口快捷键

- Ctrl+b c：创建一个新窗口，状态栏会显示多个窗口的信息。
- Ctrl+b p：切换到上一个窗口（按照状态栏上的顺序）。
- Ctrl+b n：切换到下一个窗口。
- Ctrl+b <number>：切换到指定编号的窗口，其中的<number>是状态栏上的窗口编号。
- Ctrl+b w：从列表中选择窗口。
- Ctrl+b ,：窗口重命名。
