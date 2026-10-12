Melemele_House_3_hns_MapScripts::
	.byte 0


Melemele_House3_Woman::
	lock
	faceplayer
	msgbox Melemele_House3_Woman_Text_0, MSGBOX_AUTOCLOSE
	release
	end


Melemele_House3_Man::
	lock
	faceplayer
	msgbox Melemele_House3_Man_Text_0, MSGBOX_AUTOCLOSE
	release
	end


Melemele_House3_Woman_Text_0:
	.string "החיים כאן על האי כל כך שלווים!\p"
	.string "וכיף שהנכדים שלי בקאנטו\n"
	.string "רחוקים רק שיט קצר בסירה!$"

Melemele_House3_Man_Text_0:
	.string "תיירים ארורים!\p"
	.string "המתווך שלי אמר שיהיה פה שקט…\p"
	.string "אבל כנראה שזול יותר לנסוע לכאן\n"
	.string "מאשר כל הדרך לאלולה.$"
