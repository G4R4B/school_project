open Printf

let _main = 
  (* Vérification de la ligne de commande *)
  if Array.length Sys.argv <> 2 then
    begin
      eprintf "usage: mypython file.py\n" ;
      exit 1
    end ;

   let in_file = Sys.argv.(1) in
  
  (* Vérification de l'extension .py *)
  if not (Filename.check_suffix in_file ".py") then begin
    eprintf "Le fichier d'entrée doit avoir l'extension .py\n";
    exit 1
  end;
  let out_file = Filename.chop_suffix in_file ".py" ^ ".json" in
  
  Tojson.to_json_safe in_file  |> Yojson.to_file out_file

