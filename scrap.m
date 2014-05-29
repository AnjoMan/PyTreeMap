clear all;


load cpfResults_case30_2level.mat

% simplify 'branchFaults' to structs (Python doesn't understand matlab
% objects)
for i=1:length(branchFaults),
	branchFaults{i} = branchFaults{i}.tostruct();
end


save cpfResults.mat CPFloads messages branchFaults base baseLoad

save cpfResults_case30_2level.mat CPFloads messages branchFaults base baseLoad



