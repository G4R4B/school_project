open Printf

let _main = 
  (* Vérification de la ligne de commande *)
  if Array.length Sys.argv <> 2 then
    begin
      eprintf "usage: c2json file.c\n";
      exit 1
    end;

  let in_file = Sys.argv.(1) in
  
  (* Vérification de l'extension .c *)
  if not (Filename.check_suffix in_file ".c") then begin
    eprintf "Le fichier d'entrée doit avoir l'extension .c\n";
    exit 1
  end;
  
  let out_file = Filename.chop_suffix in_file ".c" ^ ".json" in
  
  (* Convertir le fichier C en JSON *)
  Tojson.to_json_safe in_file |> Yojson.Safe.to_file out_file;
  
  (* Confirmation de la conversion *)
  (* printf "Conversion du fichier '%s' en '%s' réussie.\n" in_file out_file *)
