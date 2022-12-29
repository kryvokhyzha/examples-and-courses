-- hard

select word, count(1) as nentry
from ( 
  select regexp_split_to_table(contents, '\s') as word
  from google_file_store
) t
where word in ('bull', 'bear')
group by word
