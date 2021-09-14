def get_cd(n,x): 
	p_low = [0] 
	q_high = [0]
	q_low = [0] 
	p_high = [0] 
	maskx = 1 
	maskn = 2
	si = 2
	for i in range(256): 
		x_lowbit = (x & maskx) >> i 
		n_lowbits = (n % maskn) 
		tmppp_low = [] 
		tmpqq_low = [] 
		tmppp_high =[] 
		tmpqq_high =[] 
		x_highbit = (x >> (511-i))&1 
		n_highbits = (n)>> (1022 - 2*i) 
		for j in range(len(p_low)): 
			for pp_low in range(2): 
				for qq_low in range(2): 
					for pp_high in range(2): 
						for qq_high in range(2): 
							if pp_low ^ qq_high == x_lowbit and qq_low ^ pp_high == x_highbit:
								temp1 = ((pp_low * maskn //2 + p_low[j]) * (qq_low * maskn // 2 + q_low[j])) % maskn 
								temp2 = (((pp_high << (511-i)) + p_high[j]) * ((qq_high << (511-i)) + q_high[j]))>>(1022-2*i) 
								if temp1 == n_lowbits : 
									# if n_highbits-temp2 >= 0 and n_highbits-temp2 <=((2<<i+1)-1): 
									# 是否需要这个等号 ？ 
									# 还是说这里是一个粗略的估计 该条件只是减少了需要爆破的数目
									# 高n位的差在 2^(i+1)-1以内是 高位相同的必要条件
									if n_highbits-temp2 >= 0 and n_highbits-temp2 <=((2<<i+1)-1): 
										tmppp_low.append(pp_low * maskn //2 + p_low[j]) 
										tmpqq_low.append(qq_low * maskn //2 + q_low[j]) 
										tmppp_high.append((pp_high<<(511- i))+p_high[j]) 
										tmpqq_high.append((qq_high<<(511- i))+q_high[j]) 
		maskn *= 2 
		maskx *= 2 
		p_low = tmppp_low 
		q_low = tmpqq_low 
		p_high = tmppp_high 
		q_high = tmpqq_high 
	for a in p_low: 
		for b in p_high: 
			if n %(a+b) ==0: 
				p = a + b 
				q = n//p                                             
				return p,q


n2 = 65288148454377101841888871848806704694477906587010755286451216632701868457722848139696036928561888850717442616782583309975714172626476485483361217174514747468099567870640277441004322344671717444306055398513733053054597586090074921540794347615153542286893272415931709396262118416062887003290070001173035587341
x2 =3604386688612320874143532262988384562213659798578583210892143261576908281112223356678900083870327527242238237513170367660043954376063004167228550592110478

c = get_cd(n2,x2)[0]
print(c)