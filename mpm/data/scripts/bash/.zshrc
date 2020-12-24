
# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH="/home/dodo/.oh-my-zsh"
ZSH_THEME="robbyrussell"

#ZSH_THEME="powerlevel9k/powerlevel9k"
# Set list of themes to pick from when loading at random
# Setting this variable when ZSH_THEME=random will cause zsh to load
# a theme from this variable instead of looking in ~/.oh-my-zsh/themes/
# If set to an empty array, this variable will have no effect.
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

export TERM="xterm-256color" 

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion.
# Case-sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load?
# Standard plugins can be found in ~/.oh-my-zsh/plugins/*
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(context dir vcs)

POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(status root_indicator background_jobs history time anaconda virtualenv pyenv) #kubecontext docker_machine

POWERLEVEL9K_ANACONDA_BACKGROUND='green'


# https://github.com/robbyrussell/oh-my-zsh/wiki/Plugin:git
plugins=(
  git
  debian
  django
  cp
  pip
  python
  pep8
  pyenv
  pylint
  sudo
  docker
  docker-compose
  alias-finder
  git-auto-fetch
  vscode
  pylint
  virtualenv
  ubuntu
  themes
  history
  zsh-syntax-highlighting
  web-search
  tmux
  urltools
  command-not-found
)
apt_pref='apt'

ZSH_TMUX_AUTOSTART=true

POWERLEVEL9K_PROMPT_ON_NEWLINE=true
#POWERLEVEL9K_RPROMPT_ON_NEWLINE=true

GIT_AUTO_FETCH_INTERVAL=1200 #in seconds

source $ZSH/oh-my-zsh.sh

#DEFAULT_USER="\ue286"

#prompt_context(){}

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment

export LANG=ru_RU.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# ssh
# export SSH_KEY_PATH="~/.ssh/rsa_id"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases

# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"

alias open="xdg-open"

alias lsp='stat -c "%a %n" *'

alias sshi="ssh -o 'IdentitiesOnly=yes'"
alias locip="ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'"
alias myip='curl ipinfo.io/ip'
alias lsip='arp'

killport() { sudo lsof -t -i tcp:"$1" | xargs kill -9 ; }
alias lsports='sudo lsof -i -P -n'
alias mst='curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python -'

gtts() { gtts-cli $1 | mpg123 - }

# ru
alias ды='ls'
alias св='св'
alias lt='ls --human-readable --size -1 -S --classify'
alias mnt="mount | awk -F' ' '{ printf \"%s\t%s\n\",\$1,\$3; }' | column -t | egrep ^/dev/ | sort"
alias left='ls -t -1'
alias count='find . -type f | wc -l'

alias d2='source activate Django2'
alias dea='source deactivate'
alias pipver='pip freeze | grep'

g++r() {
    rm -f /tmp/out.a;g++ $1 -o /tmp/out.a; /tmp/out.a;
}

function peints { echo -e "\033[1;42m $1 \033[0m"; }
function peints_err { echo -e "\033[7;105;31m $1 \033[0m"; }
# mini organaze:
# pip install mdv
printmd() {
    MD_FILE=$1
    # peints "[.] Check if the package 'mdv' is installed."
    PIP_PKG=$(pip freeze | grep mdv)
    if [ -z "$PIP_PKG" ]
    then
        peints_err "[fail] Not found mdv";
        peints "[.] install mdv";
        pip install mdv;
    else
        # peints "[OK] detect $PIP_PKG"
        echo "";
    fi

    if [ -f "$MD_FILE" ]
    then
        peints "[OK] File $MD_FILE exists!";
        mdv $MD_FILE

    else
        peints_err "[fail] Not found $MD_FILE";
    fi
}
myalias-add() {
    MD_FILE="$HOME/ALIAS.md"
    ALIAS=$1
    DISCRIPTION=$2
    ALIAS_COMMAND=$(alias | grep "^$ALIAS=" | sed "s/$ALIAS=//g; s/\n/\\n" | cut -d "'" -f 2)
    # help
    if [ "$#" -lt "2" ]
    then
        echo "Used:\n\tmyalias-add [alias] [description]";
        return -1;
    fi
    # new 
    if [ ! -f "$MD_FILE" ]
    then 
        peints "[.] Create new $MD_FILE";
        echo "# Список избранных комманд:" > $MD_FILE;
        echo "| **Alias** | **Command** | **Description** |" >> $MD_FILE;
        echo "|-------|---------|-------------|" >> $MD_FILE;
    fi
    # ALIAS_COMMAND
    if [ -z "$ALIAS_COMMAND" ]
    then
        _FUNC_COMMAND=$(compgen -A function | grep "^$ALIAS")
        # is function
        if [ ! -z "$_FUNC_COMMAND" ]
        then
            peints "[.] $ALIAS is function!";
            ALIAS_COMMAND="[function]"
        else
            peints_err "[fail] Not found $ALIAS alias.";
            return -2;
        fi
    else
        peints "[OK] detect $ALIAS alias"
        echo $ALIAS_COMMAND;
    fi

    echo "| $ALIAS | $ALIAS_COMMAND | $DISCRIPTION |" >> $MD_FILE;
    peints "[OK] add $ALIAS in $MD_FILE"
}
myalias() {
    MD_FILE="$HOME/ALIAS.md"
    printmd $MD_FILE
    if [ ! -f "$MD_FILE" ]; then echo "Можете использовать 'myalias-add [Alias] [Description]' для того чтобы добавить alias в список \n[+] есть alias-finder -l"; fi
}

mysort() {
   mkdir -p pdf; mv *.pdf pdf/;
   mkdir -p torrent; mv *.torrent torrent/;
   
   mkdir -p doc; 
   mv *.doc doc/;
   mv *.docx doc/;
   mv *.ppsx doc/;
   mv *.xlsx doc/;

   mkdir -p video; 
   mv *.avi video/;
   
   

   mkdir -p img; 
   mv *.png img/;
   mv *.jpg img/;
   mv *.svg img/; 
   mv *.kra img/; 


   mkdir -p programs; 
   mv *.exe programs/;
   mv *.deb  programs/;
   mv *.sh  programs/;


   mkdir -p zip; 
   mv *.zip zip/;
   mv *.7z zip/;
   mv *.rar zip/;
   mv *.bz2 zip/;


   mkdir -p music; mv *.mp3 music/;
   
   rm *.crdownload;
   rm Thumbs.db*;
   rm *~;
   find . -empty -type d -delete;

}

# logkeys:
#alias kg='sudo ps -aux | grep "logkeys"'
#alias kgon='sudo logkeys --start --output /home/dodo/.oh-my-zsh/log/klogger.log' #TODO: fix keymaps with https://github.com/kernc/logkeys/blob/master/docs/Keymaps.md
#alias kgoff='sudo logkeys --kill'
#alias kgt='tail --follow /home/dodo/.oh-my-zsh/log/klogger.log'

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/dodo/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/dodo/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/home/dodo/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/dodo/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

alias п="git"
