[Setup]
AppName=Babbitt Quote Generator
AppVersion=1.0.0
DefaultDirName={pf}\Babbitt Quote Generator
DefaultGroupName=Babbitt Quote Generator
UninstallDisplayIcon={app}\BabbittQuoteGenerator.exe
OutputDir=dist
OutputBaseFilename=BabbittQuoteGenerator_Installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\BabbittQuoteGenerator.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\database\*"; DestDir: "{app}\database"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "dist\data\*"; DestDir: "{app}\data"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "dist\config\*"; DestDir: "{app}\config"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "dist\core\*"; DestDir: "{app}\core"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "dist\gui\*"; DestDir: "{app}\gui"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "dist\utils\*"; DestDir: "{app}\utils"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "dist\export\*"; DestDir: "{app}\export"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "dist\docs\*"; DestDir: "{app}\docs"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\Babbitt Quote Generator"; Filename: "{app}\BabbittQuoteGenerator.exe"
Name: "{commondesktop}\Babbitt Quote Generator"; Filename: "{app}\BabbittQuoteGenerator.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\BabbittQuoteGenerator.exe"; Description: "Launch Babbitt Quote Generator"; Flags: nowait postinstall skipifsilent