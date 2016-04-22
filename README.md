# anki-musthave-addons-by-ankitest

[• Must Have](https://github.com/ankitest/anki-musthave-addon-by-ankitest) is a huge compilation of numerous very useful small add-ons.

Here you can see some small interesting functionalities of [• Must Have](https://ankiweb.net/shared/info/67643234) add-on, which are published separately.

##  	• Again Hard 

<code><b><i>1996229983</i></b></code>

2 wide buttons only 
with smiles instead of words 
and a bigger font on them.
It means NO YES in any case.

NO means AGAIN anyway.
YES means HARD for Young and Mature cards
and GOOD for New, Learning and Lapses cards.

Hotkey 1 always means NO,
hotkeys 2, 3, 4 means YES anyway.

Suitable for children and newbie.

<img src="http://savepic.ru/9296115.png">

Inspired by 
<ul><li><a href="https://ankiweb.net/shared/info/1446503737" rel="nofollow">Answer Key Remap</a>,</li>
<li><a href="https://ankiweb.net/shared/info/1867966335" rel="nofollow">Bigger Show Answer Button</a>,</li>
<li><a href="https://ankiweb.net/shared/info/2494384865" rel="nofollow">Button Colours (Good, Again)</a>,</li>
<li><a href="https://ankiweb.net/shared/info/2034935033" rel="nofollow">Bigger Show <b>All</b> Answer Buttons</a>.</li></ul>
<b>upd.</b>
<i>21.04.2016</i> There is <a href="https://github.com/ankitest/anki-musthave-addons-by-ankitest/blob/master/_Again_Hard.py" rel="nofollow">Github page</a> now.
<i>09.04.2016</i> Minor code changes.
<i>05.04.2016</i> Initial issue.

No support. Use it AS IS on your own risk.

##  	• Again Hard Good Easy wide big buttons 

<code><b><i>1508882486</i></b></code>

4 wide color buttons only with smiles instead of words and a bigger font on them.

Hotkey 1 means AGAIN in any case.
Hotkey 2 means HARD when available otherwise it mean GOOD.
Hotkey 3 means GOOD anyway.
Hotkey 4 means maximum available easiness anyhow
 (it is Good for 2 buttons and Easy for 3 or 4 buttons).

<i>Show answer</i> and <i>Again Hard Good Easy</i> buttons are so wide as Anki window.

<img src="http://www.picshare.ru/uploads/160409/n67bB6G0Ud.png">

<i>Good</i> button always takes place of <i>Hard</i> and <i>Easy</i> buttons, 
if they are absent on the card.

<img src="http://s8.hostingkartinok.com/uploads/images/2016/04/d87265c89f873538cea37caf6c3787c6.png">

They are colored in compatibility with <a href="https://ankiweb.net/shared/info/1496166067" rel="nofollow">Night Color</a> addon.

<img src="http://screenshot.ru/upload/images/2016/04/09/2016-04-09_1238382b17d.png">

It is a part of <a href="https://ankiweb.net/shared/info/67643234" rel="nofollow">• Must Have</a> add-on functionality.

<img src="http://i80.fastpic.ru/big/2016/0409/52/30c8be582fa71eb9c70f3fada1d4c152.png">

You can use <a href="https://ankiweb.net/shared/info/1996229983" rel="nofollow">• Again Hard</a> addon to have only 2 answer buttons on <b>any</b> card.

<img src="http://savepic.ru/9320923.png">

Inspired by 
<ul><li><a href="https://ankiweb.net/shared/info/1446503737" rel="nofollow">Answer Key Remap</a>,</li>
<li><a href="https://ankiweb.net/shared/info/1867966335" rel="nofollow">Bigger Show Answer Button</a>,</li>
<li><a href="https://ankiweb.net/shared/info/2494384865" rel="nofollow">Button Colours (Good, Again)</a>,</li>
<li><a href="https://ankiweb.net/shared/info/2034935033" rel="nofollow">Bigger Show <b>All</b> Answer Buttons</a>.</li></ul>
<b>upd.</b>
<i>21.04.2016</i> You can visit the <a href="https://github.com/ankitest/anki-musthave-addons-by-ankitest/blob/master/_Again_Hard.py" rel="nofollow">Github page</a> now.
<i>09.04.2016</i> Initial issue.

No support. Use it AS IS on your own risk.

##  	• Alternative hotkeys to cloze selected text in Add or Editor window 

<code><i><b>2074653746</b></i></code>

It is a very simple patch 
to create additional hotkeys in <b>Add</b> and <b>Editor</b> window
<code>Ctrl+Space</code> which cloze selected text with maximum<b>+1</b> number 
and <code>Ctrl+Alt+Space</code> which cloze selected text with maximum number.

New keys are synonyms for old keys <code>Ctrl+Shift+C</code> and <code>Ctrl+Alt+Shift+C</code> respectively.

You can invent your own keys combinations, 
specify them at the beginning of the source code
and restart Anki.

<b>upd.</b>
<i>22.04.2016</i> Code is totally remastered to avoid conflict with <b>Power format pack</b>
<i>21.04.2016</i> You can follow the <a href="https://github.com/ankitest/anki-musthave-addons-by-ankitest/blob/master/_Alternative_hotkeys_to_cloze_selected_text_in_Add_or_Editor_window.py" rel="nofollow">Github page</a> now.
<i>11.04.2016</i> Initial release.

No support. Use it AS IS on your own risk.

##  • Day learning cards always before new 

<code><b><i>1331545236</i></b></code>

This is a simple monkey patch add-on that inserts day learning cards
 (learning cards with intervals that crossed the day turnover, &gt; 1440 min.)
 always before new cards without depending due reviews. 

By default Anki do so:
  <code>learning; new if before; due; day learning; new if after</code>
With this add-on card will be displayed in the following order:
  <code>learning; (day learning; new) if before; due; (day learning; new) if after</code>

Normally these cards go after due, but I want them to go before new. 

If <code>Tools -&gt; Preferences... -&gt; Basic -&gt; Show new cards before reviews</code>
   learning; day learning; new; due
If <code>Tools -&gt; Preferences... -&gt; Basic -&gt; Show new cards after reviews</code>
   learning; due; day learning; new

Now it is the part of Must Have add-on:
<a href="https://ankiweb.net/shared/info/67643234" rel="nofollow">https://ankiweb.net/shared/info/67643234</a>

inspired by Anki user rjgoif
<a href="https://ankiweb.net/shared/info/1810271825" rel="nofollow">https://ankiweb.net/shared/info/1810271825</a>
<i>put ALL due "learning" cards first ×</i>
 which does so:
  <code>learning; day learning; new if before; due; new if after</code>

<b>upd.</b>
<i>2016-04-21</i> <a href="https://github.com/ankitest/anki-musthave-addons-by-ankitest/blob/master/_Day_learning_cards_always_before_new.py" rel="nofollow">Github page</a> has been created yesterday.
<i>2016-04-09</i> Minor description changing.
<i>2016-03-18</i> Initial release.

No support. Use it AS IS on your own risk.

## • Flip-flop 

<b><i><code>519426347</code></i></b>

This is very simple add-on.

You can easily flip-flop <i>FrontSide / BackSide</i> with <b>0</b> (Zero) or <b>Insert</b> key.

<a href="http://thumbsnap.com/Li6oJ8T6" rel="nofollow" title="Image Hosted by ThumbSnap"><img src="http://thumbsnap.com/s/Li6oJ8T6.png"></a>

Use <b>Ctrl</b>+<b>PageUp</b>, <b>Ctrl</b>+<b>9</b> or <b>F7</b> 
to look at FrontSide 
of your currently visible card.

<a href="http://tinypic.com?ref=28s4j86" rel="nofollow"><img src="http://i68.tinypic.com/28s4j86.png"></a>

Use <b>Control</b>+<b>PageDown</b>, <b>Control</b>+<b>3</b> or <b>F8</b> 
to look at BackSide 
of your currently visible card.

<a href="http://www.ephotobay.com/share/anki-2016-03-02-12-10-26.html" rel="nofollow"><img src="http://www.ephotobay.com/image/anki-2016-03-02-12-10-26.jpg"></a>

<a href="https://ankiweb.net/shared/info/67643234" rel="nofollow">Must Have</a> addon already has these hotkeys.

<b>upd.</b>
<i>04/21/2016</i> Further changes in the code will be visible <a href="https://github.com/ankitest/anki-musthave-addons-by-ankitest/blame/master/_Flip-flop.py" rel="nofollow">on the Github page.</a>
<i>04/09/2016</i> Minor code changing.
<i>30.03.2016</i> Minor changes in the code.
<i>27.03.2016</i> • added in title, code is just the same.
<i>02.03.2016</i> Support "0" key.
<i>01.03.2016</i> Initial release.

No support. Use it AS IS on your own risk.

-- in Russian

Очень простое дополнение.

Вы легко можете смотреть лицевую и оборотную стороны поочерёдно, 
просто нажимая на клавишу <b>0</b> (Ноль) или <b>Insert</b>

Таком образом на цифровой клавиатуре клавиша сработает 
независимо от того, включён NumLock или нет.

<a href="http://fastpic.ru" rel="nofollow"><img src="http://i73.fastpic.ru/big/2016/0302/71/9ada1339aec3f49764fac654e6eb5c71.png"></a>

Используйте клавиши <b>Ctrl</b>+<b>PageUp</b>, <b>Ctrl</b>+<b>9</b> или <b>F7</b> 
для переключения на лицевую сторону показываемой карточки.

<img src="http://savepic.ru/8877446.png">

Используйте клавиши <b>Control</b>+<b>PageDown</b>, <b>Control</b>+<b>3</b> или <b>F8</b>
для переключения на оборотную сторону показываемой карточки.

<a href="http://www.ii4.ru/image-690738.html" rel="nofollow"><img src="http://img.ii4.ru/images/2016/03/02/690738_Anki_2016_03_02_12_04_38.png"></a>

Эта функциональность уже включена в дополнение <a href="https://ankiweb.net/shared/info/67643234" rel="nofollow"><b>Must Have</b></a>

Без поддержки. Используйте КАК ЕСТЬ на свой страх и риск.

##  	• Insensitive case type field 

<code><b><i>1616934891</i></b></code>

How to make Anki insensitive case when using <code>{{type:field}}</code>
<i>monkey patch</i>
<b>Upper case, lower case and {{type:}} </b>

Also removes trailing spaces before the comparison
and replaces non-blank space chars <code><b>&amp;nbsp;</b></code> with usual space.

And it sets up <code><i>Again</i></code> reply button as default
(which you activate by <code>Spacebar</code> or <code>Enter</code> key)
if you type wrong.

Remove <code><b>#</b></code> from line 
```
<code>
UPPER_CASE = False
#UPPER_CASE = True
</code>
```
to see upper case letters on BackSide of your cards.

You should exactly remove <code><b>#</b></code> not replace with space char
```
<code>
EXACT_COMPARING = False
#EXACT_COMPARING = True
</code>
```
if you want to do exact field comparing
(as it is done in Anki itself)
but keep spacebar functionality.

You can use it together with <a href="https://ankiweb.net/shared/info/689574440" rel="nofollow">Multiple type fields on card</a>

Inspired by <a href="https://ankiweb.net/shared/info/2074758752" rel="nofollow">Select Buttons Automatically If Correct Answer, Wrong Answer or Nothing</a>

<b>upd.</b>
<i>21.04.2016</i> You can socialize <a href="https://github.com/ankitest/anki-musthave-addons-by-ankitest/blob/master/_Insensitive_case_type_field.py" rel="nofollow">on Github page.</a>
<i>04.04.2016</i> <b>Fixed</b> <i>works as expected with</i> <code>type:</code> 
            <i>but with non-type cards it shows an error</i>
<i>03.04.2016</i> Initial release.

No support. Use it AS IS on your own risk.

##  	• Prompt and set days interval 

<code><b><i>2031109761</i></b></code>

Prompt and set days interval

<b>NB!</b> Pay attention than new interval equals <i>current interval 

plus</i> <b>+</b> Number of days until next review

(because no answer will be given).

<img src="http://i78.fastpic.ru/big/2016/0416/2c/974cdcac4dcf7ab3202301a6c9af172c.png">

Card becomes young or mature (rather if it is new or learning), 

new interval will be calculated without giving any answer.

<b>e.g.</b> If you want 2C the card in a <b>month</b>, 
you may reply with set up additional interval:
<b>30</b>   30 ±1 days
<b>4w</b>   7*4 ±3 days
<b>2m</b>   31*2 ±15 days

It is a part of <a href="https://ankiweb.net/shared/info/67643234" rel="nofollow">• Must Have</a> add-on already.

<b>upd.</b>
<i>21.04.2016</i> Talk to me on the <a href="https://github.com/ankitest/anki-musthave-addons-by-ankitest/blob/master/_Prompt_and_set_days_interval.py" rel="nofollow">Github page</a>.
<i>16.04.2016</i> Unleashed.

No support. Use it AS IS on your own risk.

## • Swap 

<code><b><i>1040866511</i></b></code>

After importing a deck do you see that some cards show the target language on the front and some on the back?

There is a way to modify a single card so the front and back are inverted:

<ol><li>install this <code><b>• Swap</b></code> add-on </li>
<li>and use <b>F12</b> in Card Reviewer</li></ol>

<img src="http://savepic.ru/9169532.png">

You can easily add your own field name pairs in existing list
(<code>Tools - Add-ons - _Swap - Edit... - Save - Restart Anki</code>):

<img src="http://i75.fastpic.ru/big/2016/0329/5e/234c89671accff7d272924cfcc77795e.png">

Pairs higher in the list take precedence over lower
if some of them exist in the same note simultaneously.

<img src="https://s9.postimg.org/rpu3ekfgf/Anki_2016-03-29_01-55-12.png">

Field names in list are case sensitive by default,
but user can define case insensitivity.
To do so go to <code>Tools ⇒ Add-ons ⇒ _Swap ⇒ Edit...</code>
and set up   <code>CASE_SENSITIVE = False</code>
then save the changes and restart Anki. 

You can swap fields also in Editor (and Add note) window, not only in Card Reviewer.
There are a <code><b>Sw</b></code> button and <code>F12</code> key for it.

<img src="https://s23.postimg.org/oms7yjmh7/Anki_2016-03-30_13-55-13.png">

<b>upd.</b>
<i>21.04.2016</i> Now this add-on <a href="https://github.com/ankitest/anki-musthave-addons-by-ankitest/blob/master/_Swap.py" rel="nofollow">is placed on Github</a> too.
<i>09.04.2016</i> Minor code changing.
<i>01.04.2016</i> Card stays on answer side after swap (F12) if it was.
<i>31.03.2016</i> Case sensitivity control variabled added.
<i>30.03.2016</i> From now you can swap fields in Editor (and Add note) window too.
<i>29.03.2016</i> Initial release

No support. Use it AS IS on your own risk.

## • Timebox tooltip 

  <b><i><code> 2014169675</code></i></b>

This is very simple addon that puts the stats when you finish a timebox in a tooltip message that goes away after a few seconds. 

<a href="http://fastpic.ru" rel="nofollow"><img src="http://i73.fastpic.ru/big/2016/0302/40/9ca55eecc0a69bc4f86b2ee81552c540.png"></a>

Tools ⇒ Preferences... (Ctrl+P) → Timebox time limit 20 mins

<a href="http://www.ii4.ru/image-690919.html" rel="nofollow"><img src="http://img.ii4.ru/images/2016/03/02/690919_Anki_2016_03_02_16_48_57.png"></a>

Thanks to unknown user for the idea. 

There is no a development page at all. Use it AS IS at your own risk.

<b>upd.</b>
<i>21.04.2016</i> <a href="https://github.com/ankitest/anki-musthave-addons-by-ankitest/blob/master/_Timebox_tooltip.py" rel="nofollow">Github page</a> is available now.
<i>27.03.2016</i> • added in title, code stays without changing.
<i>05.03.2016</i> Now <a href="https://ankiweb.net/shared/info/67643234" rel="nofollow">Must Have</a> addon also has these tooltips.

No support. Use it AS IS on your own risk.

-- in Russian

<img src="http://savepic.ru/8873396.png">

Это очень простое дополнение. Через указанное в настройках профиля время на несколько секунд в левом нижнем углу показывается всплывающая подсказка с сообщением о прошедших минутах и количестве просмотренных карточек 

<a href="http://tinypic.com?ref=1zg6ja1" rel="nofollow"><img src="http://i65.tinypic.com/1zg6ja1.png"></a>

(а не выскакивает окно в центр экрана, которое не исчезнет до тех пор, пока пользователь не нажмёт кнопку).

<a href="http://thumbsnap.com/CZN9owhS" rel="nofollow" title="Image Hosted by ThumbSnap"><img src="http://thumbsnap.com/s/CZN9owhS.png"></a>

Эта функциональность теперь включена в дополнение <a href="https://ankiweb.net/shared/info/67643234" rel="nofollow"><b>Must Have</b></a>

Без поддержки. Используйте КАК ЕСТЬ на свой страх и риск.

##  	• View HTML source with JavaScript and CSS styles 

<code><b><i>1128123950</i></b></code>

Menu <i>Cards - View Source code Body</i> <code>Alt+F3</code>
shows HTML source with JavaScript and CSS styles but <b>without jQuery</b>

Menu <i>Cards - View Source code</i> <code>Ctrl+F3</code>
shows full HTML source 

Works for decks panel, deck overview and any card.

<img src="http://savepic.ru/9351989.png">

It is a part of <a href="https://ankiweb.net/shared/info/67643234" rel="nofollow"><b>• Must Have</b></a> add-on.

<b>upd.</b>
<i>2016-04-21</i> <a href="https://github.com/ankitest/anki-musthave-addons-by-ankitest/blob/master/_View_HTML_source_with_JavaScript_and_CSS_styles.py" rel="nofollow">Github page</a> of this addon for the curious.
<i>2016-04-12</i> View <i>without jQuery</i> added.
<i>2016-04-09</i> Initial release.

<b>Please,</b> write error message on forum
<a href="https://anki.tenderapp.com/discussions/add-ons" rel="nofollow">https://anki.tenderapp.com/discussions/add-ons</a>
Site <a href="http://AnkiWeb.Net" rel="nofollow">AnkiWeb.Net</a> does not let addon's publisher/author
to reply you here in reviews (comments, remarks).
 
No support. Use it AS IS on your own risk.

##  	• Young Mature Card Fields 

<code><b><i>1751807495</i></b></code>

With this plugin you can add the following values to a template:
<ul><li>{{info:<b>Ord</b>}} - the number of the template. The first template gets the number 0, the second the number 1, etc. Useful e.g. for clozed cards, where you want Javascript code to behave different for certain cards</li>
<li>{{info:<b>Did</b>}} - the deck id</li>
<li>{{info:<b>Due</b>}} - DUE the waiting review</li>
<li>{{info:<b>Id</b>}} - the card id</li>
<li>{{info:<b>Ivl</b>}} - the current interval</li>
<li>{{info:<b>Queue</b>}} - 0=new, 1=learning, 2=due, -1=suspended, -2=buried, -3=???</li>
<li>{{info:<b>Reviews</b>}} - the amount of reviews that you had on a card</li>
<li>{{info:<b>Lapses</b>}} - the amount of lapses</li>
<li>{{info:<b>FirstReview</b>}} - the first day that this card got reviewed</li>
<li>{{info:<b>LastReview</b>}} - the last reviewed day</li>
<li>{{info:<b>TimeAvg</b>}} - the average time spent on this card</li>
<li>{{info:<b>TimeTotal</b>}} - the total time spent</li>
<li>{{info:<b>Young</b>}} - reviewed cards with Ivl &lt; 21 days</li>
<li>{{info:<b>Mature</b>}} - reviewed cards with Ivl &gt; 20 days</li>
<li>{{info:<b>CardType</b>}} -  values are 0 (suspended), 1 (maybe "learning"), 2 (normal), 3 (maybe "day learning")</li>
<li>{{info:<b>Nid</b>}} - note id</li>
<li>{{info:<b>Mod</b>}} - modified date</li>
<li>{{info:<b>Usn</b>}} - Anki increments this number each time you synchronize with AnkiWeb and applies this number to the cards that were synchronized</li>
<li>{{info:<b>Factor</b>}} - EASYNESS e.g. 2500 for 250% by default</li></ul>
To Conditional Formatting based on Maturity use Front Template:
<code>
{{Front}}
{{^info:<b>Mature</b>}}
{{hint:Back}}
{{/info:<b>Mature</b>}}
{{#info:<b>Mature</b>}}
{{type:Back}}
{{/info:<b>Mature</b>}}
</code>
If some above definitions are unclear, please check the <a href="http://ankisrs.net/docs/manual.html" rel="nofollow">manual</a>. If there are more values that you need, please write in the comments!

<code>{{<b>info:</b>Prefix}}</code> guarantees you don't see <code>{unknown field Prefix}</code> message when studying card without this add-on.

Inspired by <a href="https://ankiweb.net/shared/info/441235634" rel="nofollow">Additional Card Fields</a>

<b>upd.</b>
<i>21.04.2016</i> <a href="https://github.com/ankitest/anki-musthave-addons-by-ankitest/blob/master/_View_HTML_source_with_JavaScript_and_CSS_styles.py" rel="nofollow">Github page.</a>
<i>07.04.2016</i> Published. 

No support. Use it AS IS on your own risk.

##  	• Zooming 

<code><b><i>1071179937</i></b></code>

Your cards look like too small? That's the add-on for you!
The default font size is so big in Anki? That's 4U!

Zooms, unzooms, lets you set a 1:1 (100%) or initial (user defined) zoom level. It's pretty cool. 
Work with images as well as text.

Functions:
<ul><li>Zoom in or out with <code>Ctrl+<b>+</b>/Ctrl+<b>-</b></code></li>
<li>or with <code>Ctrl+mouse</code> wheel</li>
<li>or with the <code>View/Zoom</code> submenu.</li></ul>
It just makes the font and images a bigger size. 
U can use a bigger font or scale images if you want without this addon. 
But you don't need to adjust images and the font size 
for meeting different resolution monitor each time any more.

<img src="http://i75.fastpic.ru/big/2016/0327/72/38fdf93dd5eb2d2275b06a3015166072.png">

Improved:
<ul><li>remember user choice (also between sessions) — <b>for each profile</b> separately!</li>
<li>step ±10% (not */1.19)</li>
<li>info about current values <code>Alt+0</code></li></ul>
<img src="http://savepic.ru/9136126.png">

There are three different multipliers:
<ol><li>for decks panel</li>
<li>for deck overview</li>
<li>for cards</li></ol>
For each, there can be an user defined zoom factor set in the add-on file. 
Use <code>Tools - Add-ons - _Zooming</code> menu to edit this. 

Zoom Images simultaneously, not only text.
Images can't be zoomed more than <code>{ max-width: 95%; max-height: 95%; }</code> 
text can be zoomed min 0.1 with no max limitations.

To avoid upper limit on images 
use in <i>Styling</i> section of your cards:
<code><b>img { max-width: none; max-height: none; }</b></code>

If you need old behaviour (zoom text only),
goto <code>Tools ⇒ Add-ons ⇒ _Zooming ⇒ Edit...</code>
and set <code>ZOOM_IMAGES = False</code>
then save the changes and restart Anki. 

Essential! For small or huge screens - should be in by default.

You don't need to zoom again in every new profile. 
The zoom level can be saved.
Go to: Tools → Add-ons → _Zooming → Edit...
Then change:
<code>deck_browser_standard_zoom
overview_standard_zoom</code>
<i>and</i>
<code>review_standard_zoom</code>
each to for example 2.5 or 0.5 
then save the changes and restart Anki. 

Reply buttons in reviewer and field names in editor becomes slightly more bigger.

<img src="http://screenshot.ru/upload/images/2016/03/31/Anki_2016-03-31_16-32-010aaca.png">

Inspired by <a href="https://ankiweb.net/shared/info/2103013902" rel="nofollow">Force custom font</a>
You can play with FONT and FONTSIZE variable constants.

<img src="http://s8.hostingkartinok.com/uploads/images/2016/03/bd9eae631467882f5c3b35db3b6ac98e.png">

<b>upd.</b>
<i>21.04.2016</i> Now you can find this add-on <a href="https://github.com/ankitest/anki-musthave-addons-by-ankitest/blob/master/_Zooming.py" rel="nofollow">on Github.</a>
<i>09.04.2016</i> Minor code changing.
<i>31.03.2016</i> <a href="https://ankiweb.net/shared/info/2103013902" rel="nofollow">Force custom font</a> with font CALIBRI fontsize 16 included.
<i>30.03.2016</i> Zoom in/out images can be switched off (zoom text only as it was).
<i>29.03.2016</i> Zoom in/out images too.
<i>28.03.2016</i> Minor correction of description.
<i>27.03.2016</i> Initial issue.

Inspired by ZOOM <a href="https://ankiweb.net/shared/info/1956318463" rel="nofollow">https://ankiweb.net/shared/info/1956318463</a>

Now it is the part of Must Have add-on: 
<a href="https://ankiweb.net/shared/info/67643234" rel="nofollow">https://ankiweb.net/shared/info/67643234</a>

No support. Use it AS IS on your own risk.
