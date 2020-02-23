# Ansible managed
# zsh version: 5.4.2
# antigen version: 2.2.2
# .zshrc is for interactive shell configuration. You set options for the interactive shell there with the setopt and unsetopt commands. You can also load shell modules, set your history options, change your prompt, set up zle and completion, et cetera. You also set any variables that are only used in the interactive shell (e.g. $LS_COLORS).

# Path to your oh-my-zsh installation.
export ZSH=$HOME/.oh-my-zsh

# Set name of the theme to load. Optionally, if you set this to "random"
# it'll load a random theme each time that oh-my-zsh is loaded.
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME=""

export SHELL="/usr/bin/zsh"
export GOPATH="~/go"
export TERM="xterm-256color"
export EDITOR="vim"
export PATH="$HOME/.rbenv/bin:/usr/local/rbenv/shims:$HOME/bin:$HOME/.local/bin:$HOME/.pyenv/bin:$HOME/.rbenv/bin:$HOME/.fnm:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games"

# SOURCE: https://github.com/ajh/dotfiles/blob/master/configs/zsh/dot_zshrc
# source "before' config files
if [ -d "$HOME/.zsh.d/before" ]; then
  for z in $HOME/.zsh.d/before/*.zsh(n); do source $z; done
fi

HIST_STAMPS="yyyy-mm-dd"
UPDATE_ZSH_DAYS="30"
COMPLETION_WAITING_DOTS="true"


# ADOTDIR="$HOME/.antigen"

ANTIGEN_BUNDLES="$HOME/.antigen/bundles"
ANTIGEN_PLUGIN_UPDATE_DAYS="30"
ANTIGEN_SYSTEM_UPDATE_DAYS="30"


# The -U means mark the function vcs_info for autoloading and suppress alias expansion. The -z means use zsh (rather than ksh) style. See also the functions command.
autoload -U promptinit && promptinit

source "$HOME/.antigen/antigen/antigen.zsh"

antigen use oh-my-zsh


antigen bundle command-not-found
antigen bundle docker
antigen bundle docker-compose
antigen bundle fancy-ctrl-z
antigen bundle git-extras
antigen bundle gnu-utils
antigen bundle pip
antigen bundle systemd
antigen bundle python
antigen bundle rbenv
antigen bundle tmux
antigen bundle zsh_reload
antigen bundle tmux
antigen bundle tmuxinator
antigen bundle golang
antigen bundle ssh-agent
antigen bundle fd
antigen bundle zsh-users/zsh-autosuggestions
antigen bundle popstas/zsh-command-time
antigen bundle unixorn/autoupdate-antigen.zshplugin
antigen bundle urbainvaes/fzf-marks
antigen bundle ytet5uy4/fzf-widgets
antigen bundle zdharma/fast-syntax-highlighting
antigen bundle joel-porquet/zsh-dircolors-solarized
antigen bundle mollifier/anyframe
antigen bundle wfxr/forgit
antigen bundle eventi/noreallyjustfuckingstopalready
antigen bundle gpg-agent
antigen bundle history
antigen bundle colored-man-pages
antigen bundle bossjones/boss-git-zsh-plugin
antigen bundle bossjones/boss-docker-zsh-plugin
antigen bundle caarlos0/zsh-git-sync
antigen bundle chrissicool/zsh-256color
antigen bundle marzocchi/zsh-notify
antigen bundle willghatch/zsh-hooks
antigen bundle unixorn/git-extra-commands
antigen bundle luismayta/zsh-docker-aliases
antigen bundle luismayta/zsh-servers-functions
antigen bundle sindresorhus/pretty-time-zsh
antigen bundle mafredri/zsh-async
antigen bundle sindresorhus/pure

POWERLEVEL9K_INSTALLATION_PATH=$ANTIGEN_BUNDLES/bhilburn/powerlevel9k/powerlevel9k.zsh-theme


antigen apply

###

unsetopt share_history


autoload -Uz copy-earlier-word
zle -N copy-earlier-word

# hotkeys
bindkey '\e[1~' beginning-of-line
bindkey '\e[4~' end-of-line
bindkey '^@' fzf-select-widget
bindkey '^@.' fzf-edit-dotfiles
bindkey '^@c' fzf-change-directory
bindkey '^@f' fzf-edit-files
bindkey '^@k' fzf-kill-processes
bindkey '^@s' fzf-exec-ssh
bindkey '^\' fzf-change-recent-directory
bindkey '^r' fzf-insert-history
bindkey '^xf' fzf-insert-files
bindkey '^xd' fzf-insert-directory
bindkey '^@g' fzf-select-git-widget
bindkey '^@ga' fzf-git-add-files
bindkey '^@gc' fzf-git-change-repository
bindkey '^@gco' fzf-git-checkout-branch
bindkey '^@gd' fzf-git-delete-branches
bindkey '^@gh' fzf-select-github-widget
bindkey '^@ghi' fzf-github-show-issue
bindkey '^@ghe' fzf-github-edit-issue
bindkey '^@gho' fzf-github-open-issue
bindkey '^@ghc' fzf-github-close-issue
bindkey '^@ghco' fzf-github-comment-issue
bindkey '^@d' fzf-select-docker-widget
bindkey '^@dk' fzf-docker-kill-containers
bindkey '^@dl' fzf-docker-logs-container
bindkey '^@dr' fzf-docker-remove-containers
bindkey '^@dri' fzf-docker-remove-images
bindkey '^@drv' fzf-docker-remove-volumes
bindkey '^@dsa' fzf-docker-start-containers
bindkey '^@dso' fzf-docker-stop-containers
bindkey '^U' autosuggest-accept

# forgit
export FORGIT_FZF_DEFAULT_OPTS="
--exact
--border
--cycle
--reverse
--height '100%'
"

# fzf
export FZF_TMUX=0
export FZF_DEFAULT_OPTS="--height 100% --reverse"

# fzf-widgets: fzf-change-reset-dir
autoload -Uz chpwd_recent_dirs cdr add-zsh-hook
add-zsh-hook chpwd chpwd_recent_dirs
declare -p FZF_WIDGETS_OPTS > /dev/null 2>&1 && FZF_WIDGETS_OPTS[insert-history]="--exact"
declare -p FZF_WIDGET_OPTS > /dev/null 2>&1 && FZF_WIDGET_OPTS[insert-history]="--exact"

# zsh-autosuggestions
ZSH_AUTOSUGGEST_BUFFER_MAX_SIZE=15
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="fg=240" # gray highlight

#############################################################
# User configuration
#############################################################
export TERM="xterm-256color"

export LANG="C.UTF-8"
export LC_COLLATE="C.UTF-8"
export LC_CTYPE="C.UTF-8"
export LC_MESSAGES="C.UTF-8"
export LC_MONETARY="C.UTF-8"
export LC_NUMERIC="C.UTF-8"
export LC_TIME="C.UTF-8"
#############################################################

# ################################################################
# pure
# ################################################################
# autoload -U promptinit; promptinit

# # optionally define some options
# PURE_CMD_MAX_EXEC_TIME=10

# # change the path color
# zstyle :prompt:pure:path color white

# # change the color for both `prompt:success` and `prompt:error`
# zstyle ':prompt:pure:prompt:*' color cyan

# prompt pure
# ################################################################

# powerlevel9k
POWERLEVEL9K_SHORTEN_DIR_LENGTH=3
POWERLEVEL9K_STATUS_VERBOSE=0

POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(context dir)
POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(status background_jobs vcs command_execution_time time pyenv virtualenv)
DEFAULT_USER=$USER
POWERLEVEL9K_ALWAYS_SHOW_CONTEXT=false
POWERLEVEL9K_ALWAYS_SHOW_USER=false

POWERLEVEL9K_CUSTOM_COMMAND_TIME="zsh_command_time"
POWERLEVEL9K_CUSTOM_COMMAND_TIME_BACKGROUND="248"
POWERLEVEL9K_CUSTOM_COMMAND_TIME_FOREGROUND="000"

# https://github.com/bhilburn/powerlevel9k#command_execution_time
POWERLEVEL9K_COMMAND_EXECUTION_TIME_THRESHOLD="3"

POWERLEVEL9K_PROMPT_ON_NEWLINE=false
POWERLEVEL9K_RPROMPT_ON_NEWLINE=false
POWERLEVEL9K_PROMPT_ADD_NEWLINE=true

POWERLEVEL9K_CONTEXT_DEFAULT_FOREGROUND="255"
POWERLEVEL9K_CONTEXT_DEFAULT_BACKGROUND="024"
POWERLEVEL9K_CONTEXT_REMOTE_FOREGROUND="255"
POWERLEVEL9K_CONTEXT_REMOTE_BACKGROUND="024"
POWERLEVEL9K_CONTEXT_ROOT_FOREGROUND="255"
POWERLEVEL9K_CONTEXT_ROOT_BACKGROUND="124"

POWERLEVEL9K_DIR_DEFAULT_FOREGROUND="255"
POWERLEVEL9K_DIR_DEFAULT_BACKGROUND="240"
POWERLEVEL9K_DIR_HOME_FOREGROUND="255"
POWERLEVEL9K_DIR_HOME_BACKGROUND="240"
POWERLEVEL9K_DIR_HOME_SUBFOLDER_FOREGROUND="255"
POWERLEVEL9K_DIR_HOME_SUBFOLDER_BACKGROUND="240"

POWERLEVEL9K_VCS_CLEAN_BACKGROUND="100"
POWERLEVEL9K_VCS_MODIFIED_BACKGROUND="094"
POWERLEVEL9K_VCS_UNTRACKED_BACKGROUND="094"
POWERLEVEL9K_VCS_CLEAN_FOREGROUND="232"
POWERLEVEL9K_VCS_MODIFIED_FOREGROUND="232"
POWERLEVEL9K_VCS_UNTRACKED_FOREGROUND="232"

POWERLEVEL9K_COMMAND_EXECUTION_TIME_FOREGROUND="000"
POWERLEVEL9K_COMMAND_EXECUTION_TIME_BACKGROUND="248"

# Aliases
alias suser='su -'

# aliases
alias 'apt-update-list-upgrade'="apt update && apt upgrade --dry-run | grep Inst | sort | fzf && apt upgrade"
alias 'dfh'="df -h | grep -v docker"
alias 'ubuntu-release'="lsb_release -a"

# SOURCE: https://github.com/ajh/dotfiles/blob/master/configs/zsh/dot_zshrc
# source "after" config files
if [ -d "$HOME/.zsh.d/after" ]; then
  for z in $HOME/.zsh.d/after/*.zsh(n); do source $z; done
fi

# user configs
[[ -r /etc/zsh/zshrc.local ]] && source /etc/zsh/zshrc.local
[[ -r "$HOME/.zshrc.local" ]] && source "$HOME/.zshrc.local"

# ################################################################
# pure
# ################################################################
PURE_PROMPT_SYMBOL=❯
prompt pure
