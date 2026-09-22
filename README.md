# The Blobinator
A Python implementation of blobspeak based on the one used in [Casualties: XL](https://github.com/webbero929/CasualtiesExtra-Public/releases).
Big thanks to [MarkSuckerberg](https://github.com/MarkSuckerberg) for writing the original code.
This one feature is *the* reason that mod clicked with me as much as it does.
I have never seen a game or mod mess with my text chat in quite this way. It's simply ***wonderous***.

# Usage
To use this script, simply run blobspeak.py from the command line and pass it the text you want to input.
You may also pipe another command's output into this app ie `help | python blobspeak.py` (although note it will remove most newlines)

config.toml contains various settings that can be changed. Most of these are taken directly from Casualties: XL - if you know what a config option means there, it will mean the same thing here too. 
	for example, blobspeakModifier = the modifier slider in the mod's settings UI
config.toml is annotated with comments on what each option does.

If a word is surrounded in ^carats^ then blobspeak will not apply to it.
If burp, breath, moan are surrounded in carats like ^burp^ ^breath^ ^moan^ then they will be replaced with a burp/breath/moan. This is useful to force one into your message
# Microcommands
There are some settings that can be changed within a message.
This is done by adding them in \[square brackets\] to the start of a message.
Like this. `[mod1.5 ws8 br1] i want to be as big as a football field...`
	(That means blobspeakModifier = 1.5, weightStage = 8, brainRot = 1.0)
## Values 
### mod / blobspeakModifier
This is equivalent to the blobspeak modifier slider in the mod's config / this app's config.toml
### ws / weightStage
Ingame, this is a value from 1 to 8. (0 is possible, but useless here)
This depends on how large your character is/what set of sprites is being shown, with 8 being the largest
This is used to make your character's speech more muffled at higher weight stages
5 is the first 'immobile' stage, and the default value is 6.
### br / brainRot
This is named after an internal value. It's effectively the moan chance.
Ingame, this is anywhere from 0.0-1.0. (IIRC this is determined by gluttony)
0.5 is a reasonable default from what I've been told
**This will only have an effect if isHorny is true!**
## Booleans
### tg / Telegram mode
This will adjust formatting to be compatible with Telegram.
**Burps will not be bold in this mode due to a limitation.**
### fa / Fur Affinity mode
This will adjust formatting to be compatible with BBCode.
You probably know this as the formatting system used by Fur Affinity.

# Frontend
The AHK frontend is relatively simple.
Just run it and hit Windows + the backslash key (on American QWERTY, I think this key is shift + #. on UK QWERTY this key is the above the Windows key.) to bring up a window you can type in
Type what you want and it'll type out the blobified text.
Any  < angled brackets > in the input will be replaced with ^carats^ allowing easier use of the override and manual burp/breath/moan features.
Since this is mostly a personal project, I'm not too fussed about the lack of a frontend on other platforms.
	But if you are, and you want to do that, feel free to make a pull request! That's what they're for after all!