# 💻 CS344: Operating Systems Laboratory (July–Nov 2024)

This repository contains the **source code**, **reports**, and **solutions** for the assignments completed for the **CS344: Operating Systems Laboratory** course.  
All work is based on modifying and extending **xv6**, a simple Unix-like operating system for the x86 architecture, originally developed at MIT.

The core codebase for these assignments is derived from the official xv6 repository:  
👉 [https://github.com/mit-pdos/xv6-public](https://github.com/mit-pdos/xv6-public)

We highly recommend the accompanying textbook, which served as a primary reference for understanding the xv6 source code:  
📘 [*Operating Systems: Three Easy Pieces (OSTEP)*](https://pages.cs.wisc.edu/~remzi/OSTEP/)

---

## 👥 Group Members

The following students collaborated on the majority of these assignments:

- **Aaditya Jalan** (Roll No: 220123001)  
- **Aayush Suthar** (Roll No: 220123004)  
- **Avanish Gadhikar** (Roll No: 220123075)  
- **Chaitanya Chabra** (Roll No: 220123012)

---

## 📚 Assignments Overview

The course spanned **five major assignments (Assignment 0–4)**, each focusing on fundamental concepts of Operating Systems such as **bootstrapping, system calls, process management, scheduling, memory management**, and **file systems**.

| Assignment | Topic Area | Key Concepts Implemented |
|-------------|-------------|---------------------------|
| Assignment 0 | OS Introduction & System Calls | Inline Assembly, PC Boot Process, Custom System Calls (`draw`) |
| Assignment 1 | Process Management & Utilities | User-level `sleep`, Animation Program, Process Statistics (`wait2`) |
| Assignment 2 | Process Scheduling | Lottery Scheduler, Shortest Job First (SJF) Scheduler, Process Info System Calls |
| Assignment 3 | Memory Management & Paging | Lazy Memory Allocation, Swapping (Swap-out/Swap-in), Kernel Processes |
| Assignment 4 | File Systems Comparison | Deduplication, Large File Creation Optimization (ZFS vs. EXT4) |

---

## 📝 Assignment Solutions and Summary

---

### 🛠️ Assignment 0: OS Introduction & System Calls

This assignment served as a warm-up, covering fundamental interactions with the x86 architecture and adding a custom system call to xv6.

| Task | Summary of Implementation |
|------|----------------------------|
| **PC Boot Strap** | Traced the boot process from `0x000ffff0` (BIOS, real mode) to the boot loader at `0x7c00`. Identified the switch to 32-bit protected mode via `lgdt` and `ljmp`. |
| **Custom System Call (`draw`)** | Implemented `int draw(void *buf, uint size)` to copy ASCII art from the kernel to a user buffer. Updated all necessary kernel files (`syscall.h`, `usys.S`, `sysproc.c`, etc.) and created the user program `drawtest.c`. |

---

### ⏳ Assignment 1: Process Management & Utilities

This assignment focused on user-space utilities and gathering per-process statistics.

| Task | Summary of Implementation |
|------|----------------------------|
| **User-level sleep** | Created `user/sleep.c` to parse a command-line argument for the number of ticks and call the sleep system call. |
| **Animation Program** | Created `animate.c` using the sleep system call and screen-clearing escape sequences to display a rotating ASCII globe animation. |
| **Process Statistics (`wait2`)** | Extended `struct proc` with `ctime`, `stime`, `retime`, and `rutime`. Modified `scheduler()` to update these fields on every tick. Implemented the new system call `int wait2(int *retime, int *rutime, int *stime)` to retrieve these aggregate times for a terminated child process. |

---

### 🎰 Assignment 2: Process Scheduling

This assignment focused on implementing new scheduling algorithms (Lottery and SJF) and system calls for process information.

| Task | Summary of Implementation |
|------|----------------------------|
| **Lottery Scheduler** | Added `tickets` field to `struct proc`. Implemented the lottery logic in `scheduler()`: sum all runnable tickets, generate a winning number (`rand() % total_tickets`), and select the process whose ticket range contains the winning number. |
| **Process Info System Calls** | Implemented `settickets`, `getprocessesinfo`, `getNumProc`, `getMaxPid`, and `getProcInfo` to manage and expose process statistics and metadata from the kernel. |
| **Shortest Job First (SJF)** | Added `burst_time` field to `struct proc`. Modified `scheduler()` to iterate over all RUNNABLE processes and select the one with the minimum burst time for execution. Complexity: **Θ(n)**. |
| **Bonus: SJF Hybrid Round Robin** | Implemented a hybrid approach using a Min-Heap (Priority Queue) based on burst time. Reduced selection complexity to **O(log n)** per-step, resulting in **O(n log n)** per round. |

---

### 🧠 Assignment 3: Memory Management & Paging

This assignment implemented advanced memory management features like lazy allocation and swapping.

| Task | Summary of Implementation |
|------|----------------------------|
| **Lazy Memory Allocation** | Removed allocation logic from `sbrk()` to trigger a Page Fault (`T_PGFLT`) on first access. The kernel's trap handler catches this fault, allocates a physical page (`kalloc()`), and maps it via `mappages()`, implementing demand-driven allocation. |
| **Kernel Processes** | Implemented `create_kernel_process()` to set up privileged, kernel-only processes (no user-space context or trap frame setup), used for swapping. |
| **Swapping Mechanism** | Implemented full swapping: **Swap-Out** (moves physical pages to disk using a modified LRU policy based on the Accessed bit) and **Swap-In** (on page fault, reads page back, remaps, resumes). Used custom queues (`rqueue`, `rqueue2`) and kernel-only I/O for handling swap requests. |

---

### 💾 Assignment 4: File Systems Comparison

This assignment focused on the quantitative evaluation of modern file system features, comparing **ZFS** and **EXT4**.

| Feature & Filesystems | Benefit Quantification (ZFS vs. EXT4) | Disadvantage Quantification |
|------------------------|----------------------------------------|------------------------------|
| **Data Deduplication (ZFS feature)** | **Benefit:** Tested with *vdbench* using a 2:1 deduplication ratio (450 MB of data, half duplicates). ZFS consumed only **223 MB** of space (≈2.00× ratio). EXT4 consumed **471 MB** (no deduplication). | **Trade-offs:** ZFS showed high CPU utilization (~76.1%) and lower write performance (~77.75 MB/s) compared to EXT4 (~53.4% CPU, ~157.75 MB/s). Overhead due to deduplication hashing. |
| **Large File Creation (EXT4 optimized)** | **Benefit:** Workload of two 1 GB files — EXT4 completed in **4 s** (≈511 MB/s) using extents and delayed allocation for contiguous writes. ZFS took **16 s** (≈125.9 MB/s). | **Trade-offs:** EXT4’s extents cause greater metadata overhead for small files compared to ZFS. Also, its minimal metadata approach makes recovery from corruption more difficult. |

---

🧩 *End of README*
