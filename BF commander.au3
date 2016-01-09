#include "mousePlus.au3"
#include <GDIPlus.au3>
#include <ScreenCapture.au3>
#include <WinAPI.au3>

HotKeySet ( "å" , "end" )
HotKeySet ( "æ" , "pause")
opt("MouseClickDelay",70)
opt("WinWaitDelay",10)
opt("MouseClickDownDelay",70)
opt("MouseCoordMode",0)

$paused = False


;opt("PixelCoordMode",0)
#include <Debug.au3>
_DebugSetup("","",2)
global $winTitle = "Battlefield 4"
global $sPos[2] = [0.91,0.29]
$squadOffset = 0.034

;Give order offset
global $scanOffset = [0,-0.055]
global $empOffset = [0,-0.110]
global $giveOffset	 = [0,0.055]

;Lazy coding, avoids loops
global $specialCommands1 = [0.5*0.055,0]
global $specialCommands2 = [1.5*0.055,0]
global $specialCommands3 = [2*0.055,0]


;Area of map used in scanning
global $scanArea[4] = [0.25,0.1,0.85,0.85]

;AVG fallback rutine so it never waits on finding new red
$avgSet = 10

global $hitmap[$avgSet][2]
$hmPos = 0

WinWait ($winTitle)
$winHandle = WinGetHandle($winTitle,"")
if($winHandle = 0) then
   Exit(1)
EndIf

WinSetState($winHandle,"",@SW_SHOW)
WinActivate($winHandle)
getRedPos(1000000000000000000)

while true
   $activeWindow = WinGetHandle("[ACTIVE]")
   $mPos = MouseGetPos()
   WinActivate($winHandle)
   ;WinMove($winHandle,"",3,3,683,417)
   useUav()
   useSpec()

   orderSquads()
   Sleep(1000)
WEnd



func click($p,$key)
   ;_MouseClickPlus($Window, $Button = "left", $X = "", $Y = "", $Clicks = 1)
   $p = toCoord($p)
   MouseClick($key,$p[0],$p[1],1,0)

EndFunc

func offsetClick($root, $offset,$key = "left")
   local $p[2]

   $p[0] = $root[0] + $offset[0]
   $p[1] = $root[1] + $offset[1]
   click($p,$key)

EndFunc

func toCoord($p)
   $winInfo = WinGetPos($winHandle)
   $p[0] = $p[0]*$winInfo[2]
   $p[1] = $p[1]*$winInfo[3]
   return $p
EndFunc

func orderSquads()
   _DebugOut("Giving orders")

   $squad = Random(-2,8,1)

   $pos = $sPos
   $pos[1] = $pos[1]+$squadOffset*$squad
   click($pos,"left")
   $tar = getRedPos()
   click($tar,"right")
   offsetClick($tar,$giveOffset,"left")

EndFunc

func useSpec()
   $delay = 100

   $pos = getRedPos()
   click($pos,"right")
   Sleep($delay)
   offsetClick($pos,$specialCommands1)
   Sleep($delay)


EndFunc

func useUav()
   $delay = 100
   $pos = getRedPos()

   click($pos,"right")
   Sleep($delay)
   offsetClick($pos,$scanOffset)


   Sleep($delay)

   $pos = getRedPos()
   click($pos,"right")
   Sleep($delay)
   offsetClick($pos,$empOffset)
   Sleep($delay)


EndFunc

func getRedPos($maxTry = 10)
   $info = WinGetPos($winHandle)
   _DebugOut("Finding Red POS")
   $variation = 3
   $color = 0xFCAA85

   $p = $scanArea

   ;Converts to actual pixels

   $p[0] = $p[0]*$info[2]
   $p[1] = $p[1]*$info[3]
   $p[2] = $p[2]*$info[2]
   $p[3] = $p[3]*$info[3]


   $try = 0
   while true

	  $pattern = Random(1,4,1)

	  Switch $pattern

		 case 1
			Local $pos = PixelSearch($p[0],$p[1],$p[2],$p[3],$color,$variation,1,$winHandle)

		 case 2

			Local $pos = PixelSearch($p[2],$p[3],$p[0],$p[1],$color,$variation,1,$winHandle)

		 case 3
			Local $pos = PixelSearch($p[0],$p[3],$p[2],$p[1],$color,$variation,1,$winHandle)

		 case 4
			Local $pos = PixelSearch($p[2],$p[1],$p[0],$p[3],$color,$variation,1,$winHandle)

	  EndSwitch

	  if not @error then
		 _DebugOut("Red pos found")
		 $pos[0] = $pos[0]/$info[2]
		 $pos[1] = $pos[1]/$info[3]

		 $hitmap[$hmPos][0] = $pos[0]
		 $hitmap[$hmPos][1] = $pos[1]
		 $hmPos = Mod($hmPos + 1,$avgSet)
		 _DebugOut("Current pos in avg: " & $hmPos)

		 return $pos
	  else
		 $try = $try + 1
		 _DebugOut("Retrying...")
		 Sleep(1)

		 if($try = $maxTry) then

			local $sum[2]
			$sum[0] = 0
			$sum[1] = 0

			for $i = 0 to ($avgSet-1) step 1
			   $sum[0] = $sum[0] + $hitmap[$i][0]
			   $sum[1] = $sum[1] + $hitmap[$i][1]
			Next

			$sum[0] = $sum[0]/($avgSet)
			$sum[1] = $sum[1]/($avgSet)
			_DebugOut("Using Hitmap: x: " & $sum[0] & " y: " & $sum[1])
			return $sum
		 EndIf
	  endif
   WEnd
EndFunc



func pause()
   $paused = not $paused

   if $paused Then
	  While $paused
		 ToolTip('Script is "Paused"',0,0)
		 Sleep(10)
	  WEnd
   EndIf

EndFunc

func end()
   Exit()
EndFunc