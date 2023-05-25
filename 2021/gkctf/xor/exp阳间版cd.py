def get_cd(n,x,lenth): 
	p_low = [0] 
	q_high = [0]
	q_low = [0] 
	p_high = [0] 
	# maskn = 2
	maskn  = 0
	for i in range(lenth//2): 
		maskn = 2**(i+1)-1
		xi = (x >> i )&1
		n_lowbits = (n & maskn) 
		# 高位判断从lenth-1处开始
		High_index = lenth-1 -i
		XHi = (x >> (High_index))&1 
		n_highbits = (n)>> (High_index) *2
		nextP_l = [] 
		nextQ_l = [] 
		nextP_h =[] 
		nextQ_h =[] 
		
		for j in range(len(p_low)): 
			for pl in range(2): 
				for ql in range(2): 
					for ph in range(2): 
						for qh in range(2): 
							if pl ^ qh == xi and ql ^ ph == XHi:
								PlxQl = (((pl<<i) + p_low[j]) * ((ql<<i) + q_low[j])) & maskn 
								PhxQh = (((ph << (High_index)) + p_high[j]) * ((qh << (High_index)) + q_high[j]))>>(High_index)*2 
								if PlxQl == n_lowbits : 
									# if n_highbits-PhxQh >= 0 and n_highbits-PhxQh <=((2<<i+1)-1): 
									# 是否需要这个等号 ？ 
									# 还是说这里是一个粗略的估计 该条件只是减少了需要爆破的数目
									# 高n位的差在 2^(i+1)-1以内是 高位相同的必要条件
									if n_highbits-PhxQh >= 0 and n_highbits-PhxQh <=((2<<i+1)-1): 
										nextP_l.append((pl<<i) + p_low[j]) 
										nextQ_l.append((ql<<i) + q_low[j]) 
										nextP_h.append((ph<<(High_index))+p_high[j]) 
										nextQ_h.append((qh<<(High_index))+q_high[j]) 
		p_low = nextP_l 
		q_low = nextQ_l 
		p_high = nextP_h 
		q_high = nextQ_h 
	for a in p_low: 
		for b in p_high: 
			if n %(a+b) ==0: 
				p = a + b 
				q = n//p                                             
				print(p,q)
				break


n2 = 65288148454377101841888871848806704694477906587010755286451216632701868457722848139696036928561888850717442616782583309975714172626476485483361217174514747468099567870640277441004322344671717444306055398513733053054597586090074921540794347615153542286893272415931709396262118416062887003290070001173035587341
x2 =3604386688612320874143532262988384562213659798578583210892143261576908281112223356678900083870327527242238237513170367660043954376063004167228550592110478
lenth = 512
get_cd(n2,x2,lenth)

# ic(p,q)