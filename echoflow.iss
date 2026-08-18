[Setup]
AppName=EchoFlow
AppVersion=0.1.0
AppPublisher=EchoFlow Authors
DefaultDirName={autopf}\EchoFlow
DefaultGroupName=EchoFlow
OutputBaseFilename=EchoFlowSetup
Compression=lzma2/ultra64
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
SetupIconFile=compiler:SetupClassicIcon.ico
UninstallDisplayIcon={app}\EchoFlow.exe

[Files]
Source: "dist\EchoFlow\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\EchoFlow"; Filename: "{app}\EchoFlow.exe"
Name: "{group}\Uninstall EchoFlow"; Filename: "{uninstallexe}"
Name: "{autodesktop}\EchoFlow"; Filename: "{app}\EchoFlow.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
Filename: "{app}\EchoFlow.exe"; Description: "Launch EchoFlow"; Flags: nowait postinstall skipifsilent
