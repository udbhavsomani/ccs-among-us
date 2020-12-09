"use strict";

var live_user = (function() {
    var user = $.parseJSON($.ajax({
        type: 'POST',
        url: '/terminal',
        data: { 'command': 'get_teamname' },
        async: false,
    }).responseText);

    return user.user;
})();

/**
 * Configs
 */
var configs = (function() {
    var instance;
    var Singleton = function(options) {
        var options = options || Singleton.defaultOptions;
        for (var key in Singleton.defaultOptions) {
            this[key] = options[key] || Singleton.defaultOptions[key];
        }
    };

    Singleton.defaultOptions = {
        general_help: "Below there's a list of commands that you can use.\nYou can use autofill by pressing the TAB key, autocompleting if there's only 1 possibility, or showing you a list of possibilities.",
        ls_help: "List information about the files and folders (the current directory by default).",
        cat_help: "Read FILE(s) content and print it to the standard output (screen).",
        whoami_help: "Print the user name associated with the current effective user ID and more info.",
        date_help: "Print the system date and time.",
        logout_help: "To logout of your terminal.",
        transactions_help: "Show all your transactions.",
        submit_answer_help: "To submit your answer for a question.",
        help_help: "Print this menu.",
        clear_help: "Clear the terminal screen.",
        reboot_help: "Reboot the system.",
        cd_help: "Change the current working directory.",
        mv_help: "Move (rename) files.",
        rm_help: "Remove files or directories.",
        rmdir_help: "Remove directory, this command will only work if the folders are empty.",
        touch_help: "Change file timestamps. If the file doesn't exist, it's created an empty one.",
        sudo_help: "Execute a command as the superuser.",
        whs_help: "Who Has Solved a particular question correctly.",
        coins_help: "Displays your wallet",
        send_help: "Used to send coins to another team",
        report_help: "Used to report another team if you think they are imposters",
        ganswer_help: "Used to send answer to other teams after deal",
        ranswer_help: "Shows all the answers that you have recieved from other teams",
        leaderboard_help: "Shows current leaderboard",
        insert_question_help: "Admin only command",
        at_help: "Admin only command",
        al_help: "Admin only command",
        welcome: "Welcome to CodeSus! :)\nNow in order to get started, feel free to either execute the 'help' command or use the more user-friendly sidenav at your left.\nIn order to skip text rolling, double click/touch anywhere.\nBest of luck!",
        internet_explorer_warning: "NOTE: I see you're using internet explorer, this website won't work properly.",
        welcome_file_name: "welcome_message.txt",
        invalid_command_message: "<value>: command not found.",
        reboot_message: "Preparing to reboot...\n\n3...\n\n2...\n\n1...\n\nRebooting...\n\n",
        permission_denied_message: "Unable to '<value>', permission denied.",
        sudo_message: "Unable to sudo using a web client.",
        coins_message: "You currently have ",
        logout_message: "Logging you out....!",
        transaction_message: "Your transactions: \n",
        usage: "Usage",
        file: "file",
        file_not_found: "File '<value>' not found.",
        username: "Username",
        hostname: "Host",
        platform: "Platform",
        accesible_cores: "Accessible cores",
        language: "Language",
        value_token: "<value>",
        host: "ccstiet.com",
        user: "User",
        is_root: true,
        type_delay: 20
    };
    return {
        getInstance: function(options) {
            instance === void 0 && (instance = new Singleton(options));
            return instance;
        }
    };
})();

/**
 * Your files here
 */
var files = (function() {
    var instance;
    var Singleton = function(options) {
        var options = options || Singleton.defaultOptions;
        for (var key in Singleton.defaultOptions) {
            this[key] = options[key] || Singleton.defaultOptions[key];
        }
    };
    Singleton.defaultOptions = {
        "about.txt": "Some cliche Description of this event.",
        "rulebook.txt": "Here are the rules and guidelines for the event:\n\n1.	CodeSus is a team event with minimum 2 and maximum 3 members.\n\n2.	It is an intra college event therefore the team should consist of only Thapar students.\n\n3.	The questions will be of simple coding, aptitude and CTF type.\n\n4.	The website has a terminal like interface. You can type the 'help' command to view the list of various other commands. \n\nFor example: To view the leaderboard, type “leaderboard” or to view which team has answered correctly, type “whs”.\n\n5.	A new question will appear after every 15 minutes on the side panel. A pop-up screen will appear where one member of your team has to submit the answer. Each correct answer fetches your team 100 points and 100 coins.\n\n6.	Both points and coins will be considered while evaluating the final scores.\n\n7.	Once a team has submitted the correct answer, it has the choice to trade its answer with another team for coins. It is up to you if you trade the correct answer or an incorrect one.\n\n8.	If the team purchasing the answer finds it suspicious, it can report the selling team BEFORE submitting an answer for that particular question. \n\n9.	If the report is successful, the reporting team will get 70% of their transaction value back (i.e. coins) and they will also get a bonus score of 50 points for a successful report. \n\n10.	The team which gets reported, 150% of the transaction value (i.e. coins) will be deducted.\n\n11.	If the report is unsuccessful (the answer received was correct but team was reported), the reporting team will not get any points for submitting that answer.\n\n12.	You can trade with a particular team only once for a particular question.\n\n13.	The entire event will be conducted on Airmeet where all the trading will take place.\n\n14.	Follow @ccs_tiet on Instagram for updates.\n\n15.	Join the CodeSus Discord server: https://discord.gg/GyBYpJcXJr",
        "getting_started.txt": "Type 'help'",
        "contact.txt": "ccs@thapar.edu",
    };
    $.ajax({
        type: 'POST',
        url: '/terminal',
        async: false,
        data: { 'command': 'show_question' },
        success: function(data) {
            for (let x in data.data) {
                let ques = "question" + x.toString() + ".txt";
                Singleton.defaultOptions[ques] = data.data[x];
            }
        },
        error: function() {}
    });
    return {
        getInstance: function(options) {
            instance === void 0 && (instance = new Singleton(options));
            return instance;
        }
    };
})();

var main = (function() {

    /**
     * Aux functions
     */
    var isUsingIE = window.navigator.userAgent.indexOf("MSIE ") > 0 || !!navigator.userAgent.match(/Trident.*rv\:11\./);

    var ignoreEvent = function(event) {
        event.preventDefault();
        event.stopPropagation();
    };

    var scrollToBottom = function() {
        window.scrollTo(0, document.body.scrollHeight);
    };

    var isURL = function(str) {
        return (str.startsWith("http") || str.startsWith("www")) && str.indexOf(" ") === -1 && str.indexOf("\n") === -1;
    };

    /**
     * Model
     */
    var InvalidArgumentException = function(message) {
        this.message = message;
        // Use V8's native method if available, otherwise fallback
        if ("captureStackTrace" in Error) {
            Error.captureStackTrace(this, InvalidArgumentException);
        } else {
            this.stack = (new Error()).stack;
        }
    };
    // Extends Error
    InvalidArgumentException.prototype = Object.create(Error.prototype);
    InvalidArgumentException.prototype.name = "InvalidArgumentException";
    InvalidArgumentException.prototype.constructor = InvalidArgumentException;

    var cmds = {
        WHS: { value: "whs", help: configs.getInstance().whs_help },
        AL: { value: "al", help: configs.getInstance().al_help },
        AT: { value: "at", help: configs.getInstance().at_help },
        INSERT_QUESTION: { value: "insert_question", help: configs.getInstance().insert_question_help },
        SUBMIT_ANSWER: { value: "submit_answer", help: configs.getInstance().submit_answer_help },
        TRANSACTIONS: { value: "transactions", help: configs.getInstance().transactions_help },
        LOGOUT: { value: "logout", help: configs.getInstance().logout_help },
        LS: { value: "ls", help: configs.getInstance().ls_help },
        COINS: { value: "coins", help: configs.getInstance().coins_help },
        SEND: { value: "send", help: configs.getInstance().send_help },
        REPORT: { value: "report", help: configs.getInstance().report_help },
        GANSWER: { value: "ganswer", help: configs.getInstance().ganswer_help },
        RANSWER: { value: "ranswer", help: configs.getInstance().ranswer_help },
        LEADERBOARD: { value: "leaderboard", help: configs.getInstance().leaderboard_help },
        CAT: { value: "cat", help: configs.getInstance().cat_help },
        WHOAMI: { value: "whoami", help: configs.getInstance().whoami_help },
        DATE: { value: "date", help: configs.getInstance().date_help },
        HELP: { value: "help", help: configs.getInstance().help_help },
        CLEAR: { value: "clear", help: configs.getInstance().clear_help },
        REBOOT: { value: "reboot", help: configs.getInstance().reboot_help },
        CD: { value: "cd", help: configs.getInstance().cd_help },
        MV: { value: "mv", help: configs.getInstance().mv_help },
        RM: { value: "rm", help: configs.getInstance().rm_help },
        RMDIR: { value: "rmdir", help: configs.getInstance().rmdir_help },
        TOUCH: { value: "touch", help: configs.getInstance().touch_help },
        SUDO: { value: "sudo", help: configs.getInstance().sudo_help }
    };

    var Terminal = function(prompt, cmdLine, output, sidenav, profilePic, user, host, root, outputTimer) {
        if (!(prompt instanceof Node) || prompt.nodeName.toUpperCase() !== "DIV") {
            throw new InvalidArgumentException("Invalid value " + prompt + " for argument 'prompt'.");
        }
        if (!(cmdLine instanceof Node) || cmdLine.nodeName.toUpperCase() !== "INPUT") {
            throw new InvalidArgumentException("Invalid value " + cmdLine + " for argument 'cmdLine'.");
        }
        if (!(output instanceof Node) || output.nodeName.toUpperCase() !== "DIV") {
            throw new InvalidArgumentException("Invalid value " + output + " for argument 'output'.");
        }
        if (!(sidenav instanceof Node) || sidenav.nodeName.toUpperCase() !== "DIV") {
            throw new InvalidArgumentException("Invalid value " + sidenav + " for argument 'sidenav'.");
        }
        if (!(profilePic instanceof Node) || profilePic.nodeName.toUpperCase() !== "IMG") {
            throw new InvalidArgumentException("Invalid value " + profilePic + " for argument 'profilePic'.");
        }

        (typeof user === "string" && typeof host === "string") && (this.completePrompt = live_user + "@" + host + ":~" + (root ? "#" : "$"));
        this.profilePic = profilePic;
        this.prompt = prompt;
        this.cmdLine = cmdLine;
        this.output = output;
        this.sidenav = sidenav;
        this.sidenavOpen = false;
        this.sidenavElements = [];
        this.typeSimulator = new TypeSimulator(outputTimer, output);
    };

    Terminal.prototype.type = function(text, callback) {
        this.typeSimulator.type(text, callback);
    };

    Terminal.prototype.exec = function() {
        var command = this.cmdLine.value;
        this.cmdLine.value = "";
        this.prompt.textContent = "";
        this.output.innerHTML += "<span class=\"prompt-color\">" + this.completePrompt + "</span> " + command + "<br/>";
    };

    Terminal.prototype.init = function() {
        this.sidenav.addEventListener("click", ignoreEvent);
        this.cmdLine.disabled = true;
        this.sidenavElements.forEach(function(elem) {
            elem.disabled = true;
        });
        this.prepareSideNav();
        this.lock(); // Need to lock here since the sidenav elements were just added
        document.body.addEventListener("click", function(event) {
            if (this.sidenavOpen) {
                this.handleSidenav(event);
            }
            this.focus();
        }.bind(this));
        this.cmdLine.addEventListener("keydown", function(event) {
            if (event.which === 13 || event.keyCode === 13) {
                this.handleCmd();
                ignoreEvent(event);
            } else if (event.which === 9 || event.keyCode === 9) {
                this.handleFill();
                ignoreEvent(event);
            }
        }.bind(this));
        this.reset();
    };

    Terminal.makeElementDisappear = function(element) {
        element.style.opacity = 0;
        element.style.transform = "translateX(-300px)";
    };

    Terminal.makeElementAppear = function(element) {
        element.style.opacity = 1;
        element.style.transform = "translateX(0)";
    };

    Terminal.prototype.prepareSideNav = function() {
        var capFirst = (function() {
            return function(string) {
                return string.charAt(0).toUpperCase() + string.slice(1);
            }
        })();
        for (var file in files.getInstance()) {
            var element = document.createElement("button");
            Terminal.makeElementDisappear(element);
            element.onclick = function(file, event) {
                this.handleSidenav(event);
                this.cmdLine.value = "cat " + file + " ";
                this.handleCmd();
            }.bind(this, file);
            element.appendChild(document.createTextNode(capFirst(file.replace(/\.[^/.]+$/, "").replace(/_/g, " "))));
            this.sidenav.appendChild(element);
            this.sidenavElements.push(element);
        }
        // Shouldn't use document.getElementById but Terminal is already using loads of params
        document.getElementById("sidenavBtn").addEventListener("click", this.handleSidenav.bind(this));
    };

    Terminal.prototype.handleSidenav = function(event) {
        if (this.sidenavOpen) {
            this.profilePic.style.opacity = 0;
            this.sidenavElements.forEach(Terminal.makeElementDisappear);
            this.sidenav.style.width = "50px";
            document.getElementById("sidenavBtn").innerHTML = "&#9776;";
            this.sidenavOpen = false;
        } else {
            this.sidenav.style.width = "300px";
            this.sidenavElements.forEach(Terminal.makeElementAppear);
            document.getElementById("sidenavBtn").innerHTML = "&times;";
            this.profilePic.style.opacity = 1;
            this.sidenavOpen = true;
        }
        document.getElementById("sidenavBtn").blur();
        ignoreEvent(event);
    };

    Terminal.prototype.lock = function() {
        this.exec();
        this.cmdLine.blur();
        this.cmdLine.disabled = true;
        this.sidenavElements.forEach(function(elem) {
            elem.disabled = true;
        });
    };

    Terminal.prototype.unlock = function() {
        this.cmdLine.disabled = false;
        this.prompt.textContent = this.completePrompt;
        this.sidenavElements.forEach(function(elem) {
            elem.disabled = false;
        });
        scrollToBottom();
        this.focus();
    };

    Terminal.prototype.handleFill = function() {
        var cmdComponents = this.cmdLine.value.trim().split(" ");
        if ((cmdComponents.length <= 1) || (cmdComponents.length === 2 && cmdComponents[0] === cmds.CAT.value)) {
            this.lock();
            var possibilities = [];
            if (cmdComponents[0].toLowerCase() === cmds.CAT.value) {
                if (cmdComponents.length === 1) {
                    cmdComponents[1] = "";
                }
                if (configs.getInstance().welcome_file_name.startsWith(cmdComponents[1].toLowerCase())) {
                    possibilities.push(cmds.CAT.value + " " + configs.getInstance().welcome_file_name);
                }
                for (var file in files.getInstance()) {
                    if (file.startsWith(cmdComponents[1].toLowerCase())) {
                        possibilities.push(cmds.CAT.value + " " + file);
                    }
                }
            } else {
                for (var command in cmds) {
                    if (cmds[command].value.startsWith(cmdComponents[0].toLowerCase())) {
                        possibilities.push(cmds[command].value);
                    }
                }
            }
            if (possibilities.length === 1) {
                this.cmdLine.value = possibilities[0] + " ";
                this.unlock();
            } else if (possibilities.length > 1) {
                this.type(possibilities.join("\n"), function() {
                    this.cmdLine.value = cmdComponents.join(" ");
                    this.unlock();
                }.bind(this));
            } else {
                this.cmdLine.value = cmdComponents.join(" ");
                this.unlock();
            }
        }
    };

    Terminal.prototype.handleCmd = function() {
        var cmdComponents = this.cmdLine.value.trim().split(" ");
        this.lock();
        switch (cmdComponents[0]) {
            case cmds.CAT.value:
                this.cat(cmdComponents);
                break;
            case cmds.LS.value:
                this.ls();
                break;
            case cmds.WHOAMI.value:
                this.whoami();
                break;
            case cmds.DATE.value:
                this.date();
                break;
            case cmds.HELP.value:
                this.help();
                break;
            case cmds.CLEAR.value:
                this.clear();
                break;
            case cmds.REBOOT.value:
                this.reboot();
                break;
            case cmds.CD.value:
            case cmds.MV.value:
            case cmds.RMDIR.value:
            case cmds.RM.value:
            case cmds.TOUCH.value:
                this.permissionDenied(cmdComponents);
                break;
            case cmds.SUDO.value:
                this.sudo();
                break;
            case cmds.COINS.value:
                this.coins();
                break;
            case cmds.SEND.value:
                this.send();
                break;
            case cmds.REPORT.value:
                this.report();
                break;
            case cmds.GANSWER.value:
                this.ganswer();
                break;
            case cmds.RANSWER.value:
                this.ranswer();
                break;
            case cmds.LEADERBOARD.value:
                this.leaderboard();
                break;
            case cmds.LOGOUT.value:
                this.logout();
                break;
            case cmds.TRANSACTIONS.value:
                this.transactions();
                break;
            case cmds.SUBMIT_ANSWER.value:
                this.submit_answer();
                break;
            case cmds.INSERT_QUESTION.value:
                this.insert_question();
                break;
            case cmds.AT.value:
                this.at();
                break;
            case cmds.AL.value:
                this.al();
                break;
            case cmds.WHS.value:
                this.whs();
                break;
            default:
                this.invalidCommand(cmdComponents);
        };
    };

    Terminal.prototype.cat = function(cmdComponents) {
        var result;
        if (cmdComponents.length <= 1) {
            result = configs.getInstance().usage + ": " + cmds.CAT.value + " <" + configs.getInstance().file + ">";
        } else if (!cmdComponents[1] || (!cmdComponents[1] === configs.getInstance().welcome_file_name || !files.getInstance().hasOwnProperty(cmdComponents[1]))) {
            result = configs.getInstance().file_not_found.replace(configs.getInstance().value_token, cmdComponents[1]);
        } else {
            result = cmdComponents[1] === configs.getInstance().welcome_file_name ? configs.getInstance().welcome : files.getInstance()[cmdComponents[1]];
        }
        this.type(result, this.unlock.bind(this));
    };

    Terminal.prototype.ls = function() {
        var result = ".\n..\n" + configs.getInstance().welcome_file_name + "\n";
        for (var file in files.getInstance()) {
            result += file + "\n";
        }
        this.type(result.trim(), this.unlock.bind(this));
    };

    Terminal.prototype.al = function() {
        var self = this;
        let teamname, output = '';
        this.type("Enter teamname: ", () => {
            teamname = window.prompt("Enter teamname");
            $.ajax({
                type: 'POST',
                url: '/terminal',
                data: { 'command': 'al', 'teamname': teamname },
                success: function(data) {
                    if (data.error != null) {
                        self.type(data.error, self.unlock.bind(self));
                    } else {
                        for (let x in data.data) {
                            output += (data.data[x] + '\n');
                        }
                        self.type(output, self.unlock.bind(self));
                    }
                },
                error: function() {}
            });
        });
    }

    Terminal.prototype.at = function() {
        var self = this;
        let teamname, output = '';
        this.type("Enter teamname: ", () => {
            teamname = window.prompt("Enter teamname");
            $.ajax({
                type: 'POST',
                url: '/terminal',
                data: { 'command': 'at', 'teamname': teamname },
                success: function(data) {
                    if (data.error != null) {
                        self.type(data.error, self.unlock.bind(self));
                    } else {
                        for (let x in data.data) {
                            output += (data.data[x] + '\n');
                        }
                        self.type(output, self.unlock.bind(self));
                    }
                },
                error: function() {}
            });
        });
    }

    Terminal.prototype.insert_question = function() {
        var self = this;
        let q, answer;
        this.type("Enter Question: ", () => {
            q = window.prompt("Enter Question");
            this.type("Enter the answer: ", () => {
                answer = window.prompt("Enter answer");
                $.ajax({
                    type: 'POST',
                    url: '/terminal',
                    data: { 'command': 'iq', 'question': q, 'answer': answer },
                    success: function(data) {
                        if (data.error != null) {
                            self.type(data.error, self.unlock.bind(self));
                        } else {
                            self.type(data.message, self.unlock.bind(self));
                        }
                    },
                    error: function() {}
                });
            });
        });
    }

    Terminal.prototype.submit_answer = function() {
        var self = this;
        let q_num, answer;
        this.type("For question number: ", () => {
            q_num = window.prompt("Enter question number");
            this.type("Enter your answer: ", () => {
                answer = window.prompt("Enter answer");
                $.ajax({
                    type: 'POST',
                    url: '/terminal',
                    data: { 'command': 'submit', 'q_num': q_num, 'answer': answer },
                    success: function(data) {
                        if (data.error != null) {
                            self.type(data.error, self.unlock.bind(self));
                        } else if (data.status != null) {
                            self.type(data.status + " answer! " + data.message, self.unlock.bind(self));
                        } else {
                            self.type(data.message, self.unlock.bind(self));
                        }
                    },
                    error: function() {}
                });
            });
        });
    }

    Terminal.prototype.coins = function() {
        var self = this;
        $.ajax({
            type: 'POST',
            url: '/terminal',
            data: { 'command': 'get_coins' },
            success: function(data) {
                self.type(configs.getInstance().coins_message + data.coins + " coins.", self.unlock.bind(self));
            }
        });
    }

    Terminal.prototype.whs = function() {
        var self = this;
        let output = "";
        let q_num;
        this.type("Enter the question number: ", () => {
            q_num = window.prompt("Enter question number");
            $.ajax({
                type: 'POST',
                url: '/terminal',
                data: { 'command': 'whs', 'q_num': q_num },
                success: function(data) {
                    if (data.error == null) {
                        for (var x in data.data) {
                            output += (`${x}. ${data.data[x]} \n`);
                        }
                        self.type("Team Name: \n", () => {
                            self.type(output, self.unlock.bind(self));
                        });
                    } else {
                        self.type(data.error, self.unlock.bind(self));
                    }
                },
                error: function() {}
            });
        })
    }

    Terminal.prototype.send = function() {
        var self = this;
        this.type("Enter Number of coins to send:", () => {
            var coins = window.prompt("Enter Coins");
            this.type("Enter Recieving Team's Name:", () => {
                var teamName = window.prompt("Enter Team Name");
                this.type("Enter question number:", () => {
                    var q = window.prompt("Enter question number");
                    $.ajax({
                        type: 'POST',
                        url: '/terminal',
                        data: { 'command': 'transact', 'amount': coins, 'team2': teamName, 'q': q },
                        success: function(data) {
                            if (data.error != null) {
                                self.type(data.error, self.unlock.bind(self));
                            } else {
                                self.type("Sent " + coins + " coins to " + teamName + " for question " + q, self.unlock.bind(self));
                            }
                        },
                        error: function(error) {
                            console.log(error);
                        }
                    });
                });
            });
        });
    }

    Terminal.prototype.report = function() {
        var self = this;
        this.type("Enter Team Name which you want to report:", () => {
            var teamName = window.prompt("Enter Team Name");
            this.type("Enter Question Number:", () => {
                var question = window.prompt("Enter Question Number");
                this.type("Enter the answer you recieved from the team: ", () => {
                    var answer = window.prompt("Enter answer");
                    $.ajax({
                        type: 'POST',
                        url: '/terminal',
                        data: { 'command': 'report', 'team': teamName, 'answer': answer, 'q': question },
                        success: function(data) {
                            if (data.error != null) {
                                self.type(data.error, self.unlock.bind(self));
                            } else {
                                self.type(data.message, self.unlock.bind(self));
                            }

                        },
                        error: function(error) {
                            console.log(error);
                        }
                    });
                });
            });
        });
    }

    Terminal.prototype.ganswer = function() {
        var self = this;
        this.type("Enter Team Name which you want to give answer to: ", () => {
            var teamName = window.prompt("Enter Team Name");
            this.type("Enter Question Number: ", () => {
                var questionNumber = window.prompt("Enter Question Number");
                this.type("Enter answer to send: ", () => {
                    var answer = window.prompt("Enter answer");
                    $.ajax({
                        type: 'POST',
                        url: '/terminal',
                        data: { 'command': 'send_answer', 'answer': answer, 'to_team': teamName, 'question': questionNumber },
                        success: function(data) {
                            if (data.error != null) {
                                self.type(data.error, self.unlock.bind(self));
                            } else {
                                self.type(" sent answer = \"" + answer + "\" " + "to " + teamName + " for question number " + questionNumber + ".", self.unlock.bind(self));
                            }
                        },
                        error: function(error) {
                            console.log(error);
                        }
                    });
                });
            });
        });
    }

    Terminal.prototype.ranswer = function() {
        var self = this;
        let output = "";
        let q_num;
        this.type("Enter the question number for which you wish to see the received answers: ", () => {
            q_num = window.prompt("Enter question number");
            $.ajax({
                type: 'POST',
                url: '/terminal',
                data: { 'command': 'show_answers', 'q_num': q_num },
                success: function(data) {
                    if (data.error == null) {
                        for (var x in data.data) {
                            output += (data.data[x] + '\n');
                        }
                        self.type("The answers you have recieved " + "for question number " + q_num + " are: \n", () => {
                            self.type(output, self.unlock.bind(self));
                        });
                    } else {
                        self.type(data.error, self.unlock.bind(self));
                    }
                },
                error: function() {}
            });
        })
    }

    Terminal.prototype.leaderboard = function() {
        var self = this;
        let output = "";
        $.ajax({
            type: 'POST',
            url: '/terminal',
            data: { 'command': 'show_leaderboard' },
            success: function(data) {
                for (var x in data.data) {
                    output += (`${x}-------${data.data[x]} \n`);
                }
            },
            error: function() {}
        });
        self.type("****** Current Leaderboard ******\nRank----Team Name--------------------Score-----Reported\n", () => {
            this.type(output, self.unlock.bind(self));
        });
    }

    Terminal.prototype.logout = function() {
        var self = this;
        $.ajax({
            type: 'POST',
            url: '/terminal',
            data: { 'command': 'logout' },
            success: function(data) {
                self.type(configs.getInstance().logout_message, () => { window.location.href = data.url; });
            },
            error: function() {}
        });
    }

    Terminal.prototype.transactions = function() {
        var self = this;
        let output = "";
        $.ajax({
            type: 'POST',
            url: '/terminal',
            data: { 'command': 'show_transactions' },
            success: function(data) {
                for (var x in data.data) {
                    output += (data.data[x] + '\n');
                }
            },
            error: function() {}
        });
        self.type(configs.getInstance().transaction_message, () => {
            this.type(output, self.unlock.bind(self));
        });
    }

    Terminal.prototype.sudo = function() {
        this.type(configs.getInstance().sudo_message, this.unlock.bind(this));
    }

    Terminal.prototype.whoami = function(cmdComponents) {
        var result = configs.getInstance().username + ": " + live_user + "\n" + configs.getInstance().hostname + ": " + configs.getInstance().host + "\n" + configs.getInstance().platform + ": " + navigator.platform + "\n" + configs.getInstance().accesible_cores + ": " + navigator.hardwareConcurrency + "\n" + configs.getInstance().language + ": " + navigator.language;
        this.type(result, this.unlock.bind(this));
    };

    Terminal.prototype.date = function(cmdComponents) {
        this.type(new Date().toString(), this.unlock.bind(this));
    };

    Terminal.prototype.help = function() {
        var result = configs.getInstance().general_help + "\n\n";
        for (var cmd in cmds) {
            result += cmds[cmd].value + " - " + cmds[cmd].help + "\n";
        }
        this.type(result.trim(), this.unlock.bind(this));
    };

    Terminal.prototype.clear = function() {
        this.output.textContent = "";
        this.prompt.textContent = "";
        this.prompt.textContent = this.completePrompt;
        this.unlock();
    };

    Terminal.prototype.reboot = function() {
        this.type(configs.getInstance().reboot_message, () => { window.location.reload(); });
    };

    Terminal.prototype.reset = function() {
        this.output.textContent = "";
        this.prompt.textContent = "";
        if (this.typeSimulator) {
            this.type(configs.getInstance().welcome + (isUsingIE ? "\n" + configs.getInstance().internet_explorer_warning : ""), function() {
                this.unlock();
            }.bind(this));
        }
    };

    Terminal.prototype.permissionDenied = function(cmdComponents) {
        this.type(configs.getInstance().permission_denied_message.replace(configs.getInstance().value_token, cmdComponents[0]), this.unlock.bind(this));
    };

    Terminal.prototype.invalidCommand = function(cmdComponents) {
        this.type(configs.getInstance().invalid_command_message.replace(configs.getInstance().value_token, cmdComponents[0]), this.unlock.bind(this));
    };

    Terminal.prototype.focus = function() {
        this.cmdLine.focus();
    };

    var TypeSimulator = function(timer, output) {
        var timer = parseInt(timer);
        if (timer === Number.NaN || timer < 0) {
            throw new InvalidArgumentException("Invalid value " + timer + " for argument 'timer'.");
        }
        if (!(output instanceof Node)) {
            throw new InvalidArgumentException("Invalid value " + output + " for argument 'output'.");
        }
        this.timer = timer;
        this.output = output;
    };

    TypeSimulator.prototype.type = function(text, callback) {
        if (isURL(text)) {
            window.open(text);
        }
        var i = 0;
        var output = this.output;
        var timer = this.timer;
        var skipped = false;
        var skip = function() {
            skipped = true;
        }.bind(this);
        document.addEventListener("dblclick", skip);
        (function typer() {
            if (i < text.length) {
                var char = text.charAt(i);
                var isNewLine = char === "\n";
                output.innerHTML += isNewLine ? "<br/>" : char;
                i++;
                if (!skipped) {
                    setTimeout(typer, isNewLine ? timer * 2 : timer);
                } else {
                    output.innerHTML += (text.substring(i).replace(new RegExp("\n", 'g'), "<br/>")) + "<br/>";
                    document.removeEventListener("dblclick", skip);
                    callback();
                }
            } else if (callback) {
                output.innerHTML += "<br/>";
                document.removeEventListener("dblclick", skip);
                callback();
            }
            scrollToBottom();
        })();
    };

    return {
        listener: function() {
            new Terminal(
                document.getElementById("prompt"),
                document.getElementById("cmdline"),
                document.getElementById("output"),
                document.getElementById("sidenav"),
                document.getElementById("profilePic"),
                configs.getInstance().user,
                configs.getInstance().host,
                configs.getInstance().is_root,
                configs.getInstance().type_delay
            ).init();
        }
    };
})();

window.onload = main.listener;
window.onload = main.listener;