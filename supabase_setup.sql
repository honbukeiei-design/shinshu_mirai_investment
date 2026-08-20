create extension if not exists pgcrypto;

create table if not exists public.investment_submissions (
  id uuid primary key default gen_random_uuid(),
  participant_key text not null,
  team_name text not null,
  nickname text not null,
  round text not null check (round in ('first','final')),
  a_amount integer not null default 0,
  b_amount integer not null default 0,
  c_amount integer not null default 0,
  d_amount integer not null default 0,
  e_amount integer not null default 0,
  total_amount integer not null default 0 check (total_amount between 0 and 100),
  perspective text not null default '',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (participant_key, round)
);

alter table public.investment_submissions enable row level security;

drop policy if exists "investment_submissions_select" on public.investment_submissions;
drop policy if exists "investment_submissions_insert" on public.investment_submissions;
drop policy if exists "investment_submissions_update" on public.investment_submissions;

create policy "investment_submissions_select"
on public.investment_submissions for select
to anon
using (true);

create policy "investment_submissions_insert"
on public.investment_submissions for insert
to anon
with check (true);

create policy "investment_submissions_update"
on public.investment_submissions for update
to anon
using (true)
with check (true);

grant select, insert, update on public.investment_submissions to anon;
